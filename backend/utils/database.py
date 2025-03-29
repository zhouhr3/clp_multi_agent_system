from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager

from ..config.settings import settings

# 创建数据库引擎
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # 自动检测连接是否有效
    pool_recycle=3600,   # 每小时回收连接
    pool_size=10,        # 连接池大小
    max_overflow=20,     # 最大溢出连接数
    echo=False           # 是否打印SQL语句
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建线程安全的会话
ScopedSession = scoped_session(SessionLocal)

@contextmanager
def get_db_session():
    """获取数据库会话的上下文管理器"""
    session = ScopedSession()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def init_db():
    """初始化数据库"""
    from ..models.base import Base
    Base.metadata.create_all(bind=engine)

def backup_database(backup_path):
    """备份数据库"""
    import os
    import datetime
    import sqlite3
    import shutil
    
    # 仅支持SQLite数据库备份
    if 'sqlite' not in settings.DATABASE_URL:
        raise ValueError("当前仅支持SQLite数据库备份")
    
    # 获取数据库文件路径
    db_path = settings.DATABASE_URL.replace('sqlite:///', '')
    
    # 创建备份目录
    os.makedirs(backup_path, exist_ok=True)
    
    # 生成备份文件名
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_path, f"cleft_multi_agent_{timestamp}.db")
    
    # 复制数据库文件
    shutil.copy2(db_path, backup_file)
    
    return backup_file

def restore_database(backup_file):
    """从备份恢复数据库"""
    import os
    import shutil
    
    # 仅支持SQLite数据库恢复
    if 'sqlite' not in settings.DATABASE_URL:
        raise ValueError("当前仅支持SQLite数据库恢复")
    
    # 获取数据库文件路径
    db_path = settings.DATABASE_URL.replace('sqlite:///', '')
    
    # 检查备份文件是否存在
    if not os.path.exists(backup_file):
        raise FileNotFoundError(f"备份文件 {backup_file} 不存在")
    
    # 关闭所有数据库连接
    engine.dispose()
    
    # 复制备份文件到数据库文件
    shutil.copy2(backup_file, db_path)
    
    return True
