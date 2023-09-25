from fastapi import FastAPI, APIRouter, Depends, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from models.users import User
from models.hdd import HDD
from models.cpu import CPU
from models.mainboard import Mainboard, MainboardPCI
from models.ram import RAM
from models.gpu import GPU
from models.case import Case
from models.cooler import Cooler
from models.ssd import SSD
from models.quotation import Quotation
from models.programs import Program
from models.power import Power

from fastapi.responses import JSONResponse

from core.com_data import cpu_com
from core.compatibility import cpu_compatibility
from core.cpu import *
from core.common import decimal_to_name

from schemas.search import ProcessListStep1
from schemas.cpu import CPUSchema, serialize_cpu

from db.connection import engineconn

engine = engineconn()
session = engine.sessionmaker()

router = APIRouter(
    prefix="/search/cpu", # url 앞에 고정적으로 붙는 경로추가
) # Route 분리



@router.get("/{keyword:str}/{page:int}", response_model=List[CPUSchema])
async def cpu_search(keyword: str, page: int = 1, state: ProcessListStep1 = Depends()):
    cpu = session.query(CPU).filter(CPU.name.like(f'%{keyword}%')).all()
    page_size = (len(cpu) // 10) + 1
    if page > page_size:
        return JSONResponse(content={"error": "Bad Request"}, status_code=400)
    try:
        result = []

        for i in range(len(cpu)):
            item = {
                'data' : cpu[i],
                'compatibility' : [],
            }
            result.append(item)

        if state.mainboard != -1:
            mainboard = session.query(Mainboard).filter(Mainboard.id == state.mainboard).first()
            result = cpu_com_mainboard(result, mainboard)
        
        if state.ram != -1:
            ram = session.query(RAM).filter(RAM.id == state.ram).first()
            # result = [cpu for cpu in result if cpu.memory_type == ram.memory_type]
            result = cpu_com_ram(result, ram)
        
        if state.ssd != -1:
            ssd = session.query(SSD).filter(SSD.id == state.ssd).first()
            result = cpu_com_ssd(result, ssd)

        # 전체 개수 반환해줘야함
        result = sorted(result, key=lambda x: len(x["compatibility"]))
        
        for i, item in enumerate(result):
            if result[i]['data'].pcie_version == None or result[i]['data'].pcie_version == 0:
                result[i]['data'].pcie_version = []
            else:
                result[i]['data'].pcie_version = decimal_to_name(result[i]['data'].pcie_version, len(cpu_com['pcie_version']), cpu_com['pcie_version'])
            if result[i]['data'].memory_type == None or result[i]['data'].memory_type == 0:
                result[i]['data'].memory_type = []
            else:    
                result[i]['data'].memory_type = decimal_to_name(result[i]['data'].memory_type, len(cpu_com['memory_type']), cpu_com['memory_type'])
            result[i] = serialize_cpu(result[i]['data'], result[i]['compatibility'])

        headers = {"max_page": str(page_size)}

    # 데이터를 리스트에 넣을 필요가 있는 경우만 리스트로 만듦
        response = JSONResponse(content=result[(page-1)*10:min(page*10, page_size*10)], status_code=200, headers=headers)
        # response = JSONResponse(content=result, status_code=200, headers=headers)

        session.close()
        return response
    except:
        session.close()
        return JSONResponse(content={"error": "Bad Request"}, status_code=400)
    