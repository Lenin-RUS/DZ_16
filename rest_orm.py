from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, NUMERIC
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests

def parser_orm(params):
    engine = create_engine('sqlite:///orm.sqlite', echo=False)
    Base = declarative_base()

    class Area(Base):
        __tablename__ = 'area'
        id = Column(Integer, primary_key=True)
        name = Column(String, unique=True)
        def __init__(self, name):
            self.name = name

    class Trip_ready(Base):
        __tablename__ = 'trip_ready'
        id = Column(Integer, primary_key=True)
        name = Column(String, unique=True)
        def __init__(self, name):
            self.name = name

    class Education(Base):
        __tablename__ = 'education'
        id = Column(Integer, primary_key=True)
        name = Column(String, unique=True)
        def __init__(self, name):
            self.name = name

    class Schedule(Base):
        __tablename__ = 'schedule'
        id = Column(Integer, primary_key=True)
        name = Column(String, unique=True)
        def __init__(self, name):
            self.name = name

    class Skills(Base):
        __tablename__ = 'skills'
        id = Column(Integer, primary_key=True)
        name = Column(String, unique=True)
        def __init__(self, name):
            self.name = name

    class Request(Base):
        __tablename__ = 'request'
        id = Column(Integer, primary_key=True)
        area = Column(Integer, ForeignKey('area.id'))
        trip_ready = Column(Integer, ForeignKey('trip_ready.id'))
        education = Column(Integer, ForeignKey('education.id'))
        schedule = Column(Integer, ForeignKey('schedule.id'))
        request_text=Column(String)
        number_of_results=Column(Integer)

    class Skill_req(Base):
        __tablename__ = 'skill_req'
        id = Column(Integer, primary_key=True)
        skills = Column(String, ForeignKey('skills.id'))
        request = Column(String, ForeignKey('request.id'))
        skill_num = Column(Integer)
        skill_percent = Column(NUMERIC)

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    area=Area(params['area'])
    trip_ready=Trip_ready(params['business_trip_readiness'])
    education=Education(params['education_level'])
    schedule=Schedule(params['employment'])


    if session.query(Area).filter(Area.name==params['area']).count()==0:session.add(area)
    if session.query(Trip_ready).filter(Trip_ready.name==params['business_trip_readiness']).count()==0:session.add(trip_ready)
    if session.query(Education).filter(Education.name==params['education_level']).count()==0:session.add(education)
    if session.query(Schedule).filter(Schedule.name==params['employment']).count()==0:session.add(schedule)
    session.commit()

    domain='https://api.hh.ru/'
    url=f'{domain}vacancies'
    result=requests.get(url, params = params).json()
    all_found_vac=result['found']
    all_pages=result['found']//100+1 if result['found']//100 <=20 else 20

    # Подсчет скилов
    all_skills={}
    for i in range(all_pages):
        params['page']=i
        result=requests.get(url, params = params).json()
        for j in result['items']:
            rez_tmp=requests.get(j['url']).json()
            for i in rez_tmp['key_skills']:
                skill=Skills(i['name'])
                if session.query(Skills).filter(Skills.name==i['name']).count()==0:session.add(skill)
                if i['name'] in all_skills:
                    all_skills[i['name']]+=1
                else:
                    all_skills.setdefault(i['name'], 1)

    session.commit()

    request=Request()
    request.area=session.query(Area).filter(Area.name==params['area']).first().id
    request.trip_ready=session.query(Trip_ready).filter(Trip_ready.name==params['business_trip_readiness']).first().id
    request.education=session.query(Education).filter(Education.name==params['education_level']).first().id
    request.schedule=session.query(Schedule).filter(Schedule.name==params['employment']).first().id
    request.request_text=params['text']
    request.number_of_results=all_found_vac
    session.add(request)
    session.commit()

    all_keys=0
    for i in all_skills:
        all_keys += all_skills[i]

    last_ses_id=session.query(Request).order_by(Request.id.desc()).first().id

    for i in all_skills:
        skills_req=Skill_req()
        skill_num=all_skills[i]
        skill_percent=round(all_skills[i]/all_keys*100,2)
        all_skills[i] = [all_skills[i], str(round(all_skills[i]/all_keys*100,2))+'%']
        skills_req.request = last_ses_id
        skills_req.skill_num=skill_num
        skills_req.skill_percent=skill_percent
        skills_req.skills = session.query(Skills).filter(Skills.name==i).first().id
        session.add(skills_req)
        session.commit()

    all_vac=session.query(Request).order_by(Request.id.desc()).first().number_of_results

    all_skills_from_orm=[]
    for i in session.query(Skill_req, Skills).filter(Skill_req.skills==Skills.id, Skill_req.request==last_ses_id).order_by(Skill_req.skill_num.asc()).all():
        all_skills_from_orm.append([i[1].name, i[0].skill_num, i[0].skill_percent])

    session.close()

    return all_vac, all_skills_from_orm