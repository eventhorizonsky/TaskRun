from fastapi import APIRouter, Depends
from app.dependencies import success_response, error_response
from app.dependencies.auth import verify_token
import subprocess
import os
import threading

router = APIRouter()

process_store = {}
logs_store = {'process': [], 'install': []}

def add_log(log_type, line):
    logs = logs_store[log_type]
    logs.append(line)
    if len(logs) > 500:
        logs.pop(0)

def read_output(pipe, log_type):
    for line in iter(pipe.readline, ''):
        add_log(log_type, line.strip())

def install_requirements_if_exists(tasks_dir):
    req_file = os.path.join(tasks_dir, 'requirements.txt')
    if os.path.exists(req_file):
        try:
            result = subprocess.run(['pip', 'install', '-r', 'requirements.txt'], cwd=tasks_dir, capture_output=True, text=True, check=True)
            for line in result.stdout.splitlines():
                add_log('install', line)
            for line in result.stderr.splitlines():
                add_log('install', line)
            return True
        except subprocess.CalledProcessError as e:
            for line in e.stdout.splitlines():
                add_log('install', line)
            for line in e.stderr.splitlines():
                add_log('install', line)
            raise Exception(f"安装依赖失败: {e.stderr}")
    return False

@router.get('/system/health')
async def health_check():
    """健康检查接口"""
    return success_response(data={"status": "healthy"})

@router.post("/process/install", dependencies=[Depends(verify_token)])
async def install_dependencies():
    """
    安装依赖接口
    """
    tasks_dir = os.getenv('TASKS_DIR', '/workspaces/TaskRun/examleTask')
    
    def install():
        try:
            install_requirements_if_exists(tasks_dir)
        except Exception as e:
            # 错误已在 install_requirements_if_exists 中记录到日志
            pass
    
    threading.Thread(target=install).start()
    return success_response(msg="依赖安装已开始")

@router.post("/process/start", dependencies=[Depends(verify_token)])
async def start_process():
    """
    启动子进程接口
    """
    if 'taskrunner' in process_store and process_store['taskrunner'].poll() is None:
        return error_response(msg="进程已在运行")
    
    try:
        process_store['taskrunner'] = subprocess.Popen(['python', 'taskrunner.py'], cwd=os.path.dirname(__file__) + '/../..', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        threading.Thread(target=read_output, args=(process_store['taskrunner'].stdout, 'process')).start()
        threading.Thread(target=read_output, args=(process_store['taskrunner'].stderr, 'process')).start()
        return success_response(msg="进程启动成功")
    except Exception as e:
        return error_response(msg=f"启动失败: {str(e)}")

@router.post("/process/restart", dependencies=[Depends(verify_token)])
async def restart_process():
    """
    重启子进程接口
    """
    try:
        # 先停止所有相关的 taskrunner 进程
        result = subprocess.run(['pkill', '-f', 'taskrunner.py'], capture_output=True, text=True)
        
        # 清理存储的进程引用
        if 'taskrunner' in process_store:
            del process_store['taskrunner']
        
        # 再启动
        process_store['taskrunner'] = subprocess.Popen(['python', 'taskrunner.py'], cwd=os.path.dirname(__file__) + '/../..', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        threading.Thread(target=read_output, args=(process_store['taskrunner'].stdout, 'process')).start()
        threading.Thread(target=read_output, args=(process_store['taskrunner'].stderr, 'process')).start()
        return success_response(msg="进程重启成功")
    except Exception as e:
        return error_response(msg=f"重启失败: {str(e)}")

@router.post("/process/stop", dependencies=[Depends(verify_token)])
async def stop_process():
    """
    终止子进程接口
    """
    try:
        # 使用 pkill 终止所有 taskrunner.py 进程
        result = subprocess.run(['pkill', '-f', 'taskrunner.py'], capture_output=True, text=True)
        
        # 清理存储的进程引用
        if 'taskrunner' in process_store:
            del process_store['taskrunner']
        
        if result.returncode == 0 or result.returncode == 1:  # 0 表示找到并终止，1 表示未找到
            return success_response(msg="进程终止成功")
        else:
            return error_response(msg=f"终止失败: {result.stderr}")
    except Exception as e:
        return error_response(msg=f"终止失败: {str(e)}")

@router.get("/process/status", dependencies=[Depends(verify_token)])
async def get_process_status():
    """
    查询子进程状态接口
    """
    if 'taskrunner' in process_store and process_store['taskrunner'].poll() is None:
        return success_response(data={"status": "running", "pid": process_store['taskrunner'].pid})
    else:
        return success_response(data={"status": "stopped"})

@router.get('/logs', dependencies=[Depends(verify_token)])
async def get_process_logs():
    """
    查看子进程日志接口
    """
    return success_response(data={'logs': logs_store['process']})

@router.get('/install/logs', dependencies=[Depends(verify_token)])
async def get_install_logs():
    """
    查看安装日志接口
    """
    return success_response(data={'logs': logs_store['install']})