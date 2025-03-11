from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from db import Base

class Wallet(Base):
    __tablename__ = 'wallets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    wallet_id = Column(BigInteger, nullable=False)
    text = Column(Text, nullable=False)

class Reklama(Base):
    __tablename__ = 'reklama'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False)

class Vipbot(Base):
    __tablename__ = 'vip'

    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Integer, nullable=False)
    price_type = Column(String(15), nullable=False)
    expiry_date = Column(Integer, nullable=False)

class UserBot(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_chat_id = Column(BigInteger, nullable=False, unique=True)
    balans = Column(Integer, default=0, nullable=False)
    is_vip = Column(Boolean, default=False)
    vip_expiry_date = Column(DateTime, nullable=True)
    is_ban = Column(Boolean, default=False)

    def activate_vip(self, session, days=30):
        """VIP holatini faollashtirish va tugash sanasini belgilash."""
        self.is_vip = True
        self.vip_expiry_date = datetime.utcnow() + timedelta(days=days)
        session.commit()

    def check_vip_status(self, session):
        """VIP muddati tugagan bo'lsa, avtomatik o‘chiradi."""
        if self.vip_expiry_date and self.vip_expiry_date <= datetime.utcnow():
            self.is_vip = False
            self.vip_expiry_date = None
            session.commit()

class Channelforforced(Base):
    __tablename__ = 'forced_channel'

    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(BigInteger, nullable=False, unique=True)

class ChannelforBot(Base):
    __tablename__ = 'channel_for_receive'

    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(BigInteger, nullable=False, unique=True)

class Movie(Base):
    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True, autoincrement=True)
    image = Column(Text, nullable=False)
    title = Column(String(100), nullable=False)
    ganre = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    tili = Column(String(30), nullable=False)
    country = Column(String(40), nullable=False)
    film = Column(Text, nullable=True)
    code = Column(Integer, nullable=False, unique=True)

class Serial(Base):
    __tablename__ = 'serial'

    id = Column(Integer, primary_key=True, autoincrement=True)
    image = Column(Text, nullable=False)
    count_series = Column(Integer, nullable=False)
    title = Column(String(100), nullable=False)
    ganre = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    tili = Column(String(30), nullable=False)
    country = Column(String(40), nullable=False)
    code = Column(Integer, nullable=False, unique=True)

class Series(Base):
    __tablename__ = 'series'

    id = Column(Integer, primary_key=True, autoincrement=True)
    serial_id = Column(Integer, ForeignKey('serial.id'), nullable=False)
    seria = Column(Integer, nullable=False)
    part = Column(Text, nullable=False)

    serial = relationship("Serial", backref="series")
    
class Admins(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_chat_id = Column(BigInteger, nullable=False, unique=True) 