from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.db import Base
from flask_bcrypt import generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash
from sqlalchemy import Float
from werkzeug.security import generate_password_hash, check_password_hash

class Rol(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)

    # Relación 1 a muchos con User
    usuarios = relationship("User", back_populates="rol")

    # Relación muchos a muchos con Permiso usando la clase asociativa
    permisos = relationship("RolPermisos", back_populates="rol")


class Permiso(Base):
    __tablename__ = 'permisos'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)

    roles = relationship("RolPermisos", back_populates="permiso")


class RolPermisos(Base):
    __tablename__ = 'rol_permisos'

    id = Column(Integer, primary_key=True)
    rol_id = Column(Integer, ForeignKey('roles.id'))
    permiso_id = Column(Integer, ForeignKey('permisos.id'))

    # Relaciones inversas
    rol = relationship("Rol", back_populates="permisos")
    permiso = relationship("Permiso", back_populates="roles")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    telephone = Column(String(15), nullable=False)
    correo = Column(String(128), unique=True, nullable=False)
    _password = Column("password", String(256), nullable=False)

    rol_id = Column(Integer, ForeignKey('roles.id'))
    sucursal_id = Column(Integer, ForeignKey('sucursales.id'), nullable=True)

    # Relaciones
    rol = relationship("Rol", back_populates="usuarios")
    sucursal = relationship("Sucursal", back_populates="usuarios")
    ventas = relationship("SalesOrder", back_populates="usuario")

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext_password):
        self._password = generate_password_hash(plaintext_password)

    def check_password(self, password_input):
        return check_password_hash(self._password, password_input)
    
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(String(255))

    # Recursividad: relación padre-hijo
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    parent = relationship('Category', remote_side=[id], backref='subcategorias')

    # Relación 1:N con productos
    productos = relationship('Product', back_populates='categoria')
    


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)

    imagen = Column(String(255))  # ✅ NUEVO campo para URL de imagen

    category_id = Column(Integer, ForeignKey('categories.id'))
    categoria = relationship("Category", back_populates="productos")
    detalles_orden = relationship("OrderDetail", back_populates="producto")
    notas_compra = relationship("PurchaseNote", back_populates="producto")

class Sucursal(Base):
    __tablename__ = 'sucursales'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    direccion = Column(String(255), nullable=False)

    usuarios = relationship("User", back_populates="sucursal")
    ordenes = relationship("Order", back_populates="sucursal")


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    estado = Column(String(50), nullable=False, default="pendiente")
    fecha = Column(String(50), nullable=False)
    monto = Column(Float, nullable=False)

    sucursal_id = Column(Integer, ForeignKey('sucursales.id'))
    sucursal = relationship("Sucursal", back_populates="ordenes")
    detalles = relationship("OrderDetail", back_populates="order", cascade="all, delete-orphan")



class SalesOrder(Base):
    __tablename__ = 'sales_orders'

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(String(50), nullable=False)
    total = Column(Float, nullable=False)
    estado_entrega = Column(String(30), default="alistando") 
    tipo_entrega = Column(String(20), nullable=False, default="retiro")
    direccion_entrega = Column(String(255), nullable=True)

    user_id = Column(Integer, ForeignKey('users.id'))
    usuario = relationship("User", back_populates="ventas")

    payment_id = Column(Integer, ForeignKey('payment_pays.id'), nullable=True)
    pago = relationship("PaymentPay", back_populates="ventas")

class PaymentPay(Base):
    __tablename__ = 'payment_pays'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)

    ventas = relationship("SalesOrder", back_populates="pago")

    notas_compra = relationship("PurchaseNote", back_populates="pago")

class OrderDetail(Base):
    __tablename__ = 'order_details'

    id = Column(Integer, primary_key=True, index=True)
    cantidad = Column(Integer, nullable=False)
    monto = Column(Float, nullable=False)

    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))

    order = relationship("Order", back_populates="detalles")
    producto = relationship("Product", back_populates="detalles_orden")

class Supplier(Base):
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    telephone = Column(String(15), nullable=False)
    direccion = Column(String(255), nullable=False)

    notas_compra = relationship("PurchaseNote", back_populates="proveedor")

class PurchaseNote(Base):
    __tablename__ = 'purchase_notes'

    id = Column(Integer, primary_key=True, index=True)
    cantidad = Column(Integer, nullable=False)
    fecha = Column(String(50), nullable=False)
    monto = Column(Float, nullable=False)

    product_id = Column(Integer, ForeignKey('products.id'))
    supplier_id = Column(Integer, ForeignKey('suppliers.id'))
    payment_pay_id = Column(Integer, ForeignKey('payment_pays.id'))

    producto = relationship("Product", back_populates="notas_compra")
    proveedor = relationship("Supplier", back_populates="notas_compra")
    pago = relationship("PaymentPay", back_populates="notas_compra")
