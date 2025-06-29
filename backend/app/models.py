from sqlalchemy import Column, String, Text, Boolean, DateTime, Date, ForeignKey, Integer, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
import uuid

Base = declarative_base()

class Person(Base):
    __tablename__ = "people"
    
    uuid_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255))
    location = Column(String(255))
    headline = Column(String(500))
    summary = Column(Text)
    profile_url = Column(String(500))
    linkedin_url = Column(String(500))
    twitter_handle = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    experiences = relationship("Experience", back_populates="person", cascade="all, delete-orphan")
    educations = relationship("Education", back_populates="person", cascade="all, delete-orphan")
    skills = relationship("Skill", back_populates="person", cascade="all, delete-orphan")
    yale_affiliations = relationship("YaleAffiliation", back_populates="person", cascade="all, delete-orphan")
    profile_embedding = relationship("ProfileEmbedding", back_populates="person", uselist=False, cascade="all, delete-orphan")


class Experience(Base):
    __tablename__ = "experience"
    
    id = Column(Integer, primary_key=True)
    person_uuid = Column(UUID(as_uuid=True), ForeignKey("people.uuid_id", ondelete="CASCADE"))
    company = Column(String(255))
    title = Column(String(255))
    description = Column(Text)
    location = Column(String(255))
    date_from = Column(Date)
    date_to = Column(Date)
    is_current = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    person = relationship("Person", back_populates="experiences")


class Education(Base):
    __tablename__ = "education"
    
    id = Column(Integer, primary_key=True)
    person_uuid = Column(UUID(as_uuid=True), ForeignKey("people.uuid_id", ondelete="CASCADE"))
    institution = Column(String(255))
    degree = Column(String(255))
    field_of_study = Column(String(255))
    title = Column(Text)
    date_from = Column(Date)
    date_to = Column(Date)
    gpa = Column(Float)
    activities = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    person = relationship("Person", back_populates="educations")


class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True)
    person_uuid = Column(UUID(as_uuid=True), ForeignKey("people.uuid_id", ondelete="CASCADE"))
    skill_name = Column(String(100))
    endorsement_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    person = relationship("Person", back_populates="skills")


class Connection(Base):
    __tablename__ = "connections"
    
    id = Column(Integer, primary_key=True)
    person_uuid = Column(UUID(as_uuid=True), ForeignKey("people.uuid_id", ondelete="CASCADE"))
    connected_person_uuid = Column(UUID(as_uuid=True), ForeignKey("people.uuid_id", ondelete="CASCADE"))
    connection_type = Column(String(50))  # 'direct', 'second_degree', 'group_member'
    connection_source = Column(String(50))  # 'linkedin', 'twitter', 'email', 'yale_directory'
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class YaleAffiliation(Base):
    __tablename__ = "yale_affiliations"
    
    id = Column(Integer, primary_key=True)
    person_uuid = Column(UUID(as_uuid=True), ForeignKey("people.uuid_id", ondelete="CASCADE"))
    affiliation_type = Column(String(100))  # 'undergraduate', 'graduate', 'faculty', 'staff', 'alumni'
    school = Column(String(255))  # 'Yale College', 'Yale Law School', 'Yale SOM', etc.
    class_year = Column(Integer)
    residential_college = Column(String(100))
    major = Column(String(255))
    sports_teams = Column(Text)
    clubs_organizations = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    person = relationship("Person", back_populates="yale_affiliations")


class SearchQuery(Base):
    __tablename__ = "search_queries"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True))
    query_text = Column(Text)
    parsed_filters = Column(JSON)
    sql_query = Column(Text)
    result_count = Column(Integer)
    clicked_results = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ProfileEmbedding(Base):
    __tablename__ = "profile_embeddings"
    
    id = Column(Integer, primary_key=True)
    person_uuid = Column(UUID(as_uuid=True), ForeignKey("people.uuid_id", ondelete="CASCADE"), unique=True)
    embedding_text = Column(Text)
    embedding = Column(Vector(1536))  # OpenAI embeddings dimension
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    person = relationship("Person", back_populates="profile_embedding")