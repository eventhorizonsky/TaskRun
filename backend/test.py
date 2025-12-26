import asyncio  
import time  
import random  

from funboost import boost, FunctionResultStatusPersistanceConfig, BoosterParams,BrokerEnum,ctrl_c_recv,ConcurrentModeEnum  

class MyBoosterParams(BoosterParams):  
    project_name:str = '测试项目1'  # 核心配置，项目名，设置后，web接口就可以只关心某个项目下的队列，减少无关返回信息的干扰。
    broker_kind:str = BrokerEnum.REDIS
    is_send_consumer_hearbeat_to_redis : bool= True # 向redis发送心跳，这样才能从redis获取相关队列的运行信息。
    is_using_rpc_mode:bool = True # 必须设置这一个参数为True，才能支持rpc功能。
    booster_group : str = 'test_group1' # 方便按分组启动消费
    should_check_publish_func_params:bool = True # 发布消息时，是否检查消息内容是否正确，不正确的消息格式立刻从接口返回报错消息内容不正确。
    function_result_status_persistance_conf: FunctionResultStatusPersistanceConfig = FunctionResultStatusPersistanceConfig(
        is_save_result=True, is_save_status=True, expire_seconds=7 * 24 * 3600, is_use_bulk_insert=False) 


@boost(MyBoosterParams(queue_name='queue_test_g01t',qps=1,))  
def f(x):  
    time.sleep(5)  
    print(f'hi: {x}')  
    if random.random() > 0.9:  
        raise ValueError('f error')  
    return x + 1  

@boost(MyBoosterParams(queue_name='queue_test_g02t',qps=0.5,  
max_retry_times=0,))  
def f2(x,y):  
    time.sleep(2)  
    print(f'hello: {x} {y}')  
    if random.random() > 0.5:  
        raise ValueError('f2 error')  
    return x + y  

@boost(MyBoosterParams(queue_name='queue_test_g03t',qps=0.5,  
max_retry_times=0,concurrent_mode=ConcurrentModeEnum.ASYNC))  
async def aio_f3(x):  
    await asyncio.sleep(3)  
    print(f'f3aa: {x}')  
    if random.random() > 0.5:  
        raise ValueError('f3 error')  
    return x + 1 
if __name__ == '__main__':      
    f.multi_process_consume(4)  
    f2.multi_process_consume(5)    
    ctrl_c_recv()  