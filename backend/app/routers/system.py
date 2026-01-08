from fastapi import APIRouter, Depends
from app.dependencies import success_response, error_response
from app.dependencies.auth import verify_token
import subprocess
import os

router = APIRouter()

process_store = {}

def install_requirements_if_exists(tasks_dir):
    req_file = os.path.join(tasks_dir, 'requirements.txt')
    if os.path.exists(req_file):
        try:
            subprocess.run(['pip', 'install', '-r', 'requirements.txt'], cwd=tasks_dir, check=True)
            return True
        except subprocess.CalledProcessError as e:
            raise Exception(f"安装依赖失败: {str(e)}")
    return False

@router.get('/system/health')
async def health_check():
    """健康检查接口"""
    return success_response(data={"status": "healthy"})

@router.post("/process/start", dependencies=[Depends(verify_token)])
async def start_process():
    """
    启动子进程接口
    """
    if 'taskrunner' in process_store and process_store['taskrunner'].poll() is None:
        return error_response(msg="进程已在运行")
    
    tasks_dir = os.getenv('TASKS_DIR', '/workspaces/TaskRun/examleTask')
    try:
        install_requirements_if_exists(tasks_dir)
        process_store['taskrunner'] = subprocess.Popen(['python', 'taskrunner.py'], cwd=os.path.dirname(__file__) + '/../..')
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
        
        # 检查并安装依赖
        tasks_dir = os.getenv('TASKS_DIR', '/workspaces/TaskRun/examleTask')
        install_requirements_if_exists(tasks_dir)
        
        # 再启动
        process_store['taskrunner'] = subprocess.Popen(['python', 'taskrunner.py'], cwd=os.path.dirname(__file__) + '/../..')
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