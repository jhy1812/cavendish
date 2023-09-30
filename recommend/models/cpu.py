from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class CPU(Base):
    __tablename__ = 'cpu'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    price = Column(Integer)
    link = Column(String(500), nullable=False)
    company = Column(String(30), nullable=False)
    product_seq = Column(Integer, nullable=False)
    image = Column(String(500), nullable=True, comment='이미지 링크')
    code = Column(String(30), nullable=True)
    socket = Column(String(30), nullable=False, comment='호환성')
    core_number = Column(Integer)
    thread_number = Column(Integer)
    l2_cache = Column(Integer, comment='단위: MB')
    l3_cache = Column(Integer, comment='단위: MB')
    tdp = Column(Integer, comment='발열관련 표시단위: W')
    pbpmtp = Column(Integer, comment='단위: W')
    has_graphic = Column(Boolean, comment='0: 없음, 1: 있음')
    graphic_name = Column(String(100))
    graphic_core_speed = Column(Integer, comment='단위: MHz')
    memory_capacity = Column(Integer, comment='단위: GB')
    memory_type = Column(Integer, comment='호환성, 비트마스킹')
    memory_clock = Column(Integer, comment='단위: MHz')
    memory_channel = Column(Integer)
    pcie_version = Column(Integer, comment='호환성, 비트마스킹')
    pcie_channel_number = Column(Integer)
    has_cooler = Column(Boolean, comment='0: 없음, 1: 있음')
    clock_basic = Column(Float, comment='단위: GHz')
    clock_max = Column(Float, comment='단위: GHz')
    nm = Column(Integer, comment='단위: nm')
    tech_support = Column(String(100))
    bench_mark = Column(Integer)
    reg_date = Column(Integer, comment='yyyymm')
    bookmark = Column(Integer, default=0)

    requirments = relationship("Requirements", back_populates="cpu", lazy='dynamic')