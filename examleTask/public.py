
import asyncio  
import time  
import random
import typing  

from funboost import boost, FunctionResultStatusPersistanceConfig, BoosterParams,BrokerEnum,ctrl_c_recv,ConcurrentModeEnum  
from funboost.contrib.save_function_result_status.save_result_status_to_sqldb import save_result_status_to_sqlalchemy

class MyBoosterParams(BoosterParams):  
    project_name:str = '新的测试项目'  # 核心配置，项目名，设置后，web接口就可以只关心某个项目下的队列，减少无关返回信息的干扰。
    broker_kind:str = BrokerEnum.REDIS
    is_send_consumer_heartbeat_to_redis : bool= True # 向redis发送心跳，这样才能从redis获取相关队列的运行信息。
    is_using_rpc_mode:bool = True # 必须设置这一个参数为True，才能支持rpc功能。
    booster_group : str = 'test_group1' # 方便按分组启动消费
    user_custom_record_process_info_func=save_result_status_to_sqlalchemy
    should_check_publish_func_params:bool = False