from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    STATUS = [("ACTIVE", "Active"), ("INACTIVE", "Inactive")]
    status = models.CharField(max_length=10, choices=STATUS, default="ACTIVE")
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    deleted_at = models.DateTimeField(null=True, blank=True) 

    class Meta:
        abstract = True 


class direccion(BaseModel):
    calle = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    depto = models.CharField(max_length=10, blank=True, null=True)
    comuna = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'direccion'
        managed = True


class roles(BaseModel):
    nombre = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'roles'
        managed = True


class departamento(BaseModel):
    nombre = models.CharField(max_length=45)
    description = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'departamento'
        managed = True

    # --------- agregado ---------
    def __str__(self):
        return self.nombre
    # ----------------------------


class cargo(BaseModel):
    nombre = models.CharField(max_length=45)
    description = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'cargo'
        managed = True

    # --------- agregado ---------
    def __str__(self):
        return self.nombre
    # ----------------------------


class empleado(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    run = models.CharField(max_length=45, unique=True)
    fono = models.IntegerField(blank=True, null=True)
    nacionalidad = models.CharField(max_length=45, blank=True, null=True)

    cargo = models.ForeignKey(
        cargo,                       # tu modelo está en minúsculas
        on_delete=models.SET_NULL,   # si borran el cargo, no borres al empleado
        null=True, blank=True,
        related_name="empleados"
    )
    
    
    # ⬇️ NUEVO: vínculo a ZonaTrabajo
    zona_trabajo = models.ForeignKey(
        'ZonaTrabajo',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='empleados'
    )


    class Meta:
        db_table = 'empleado'
        managed = True

    # --------- agregado ---------
    def __str__(self):
        # Muestra RUN y nombre completo si existe, si no username
        full_name = (self.user.get_full_name() or "").strip()
        return f"{self.run} — {full_name or self.user.username}"
    # ----------------------------


class cuenta_bancaria(BaseModel):
    banco = models.CharField(max_length=45)
    tipo_cuenta = models.CharField(max_length=45)
    numero_cuenta = models.BigIntegerField()
    correo = models.CharField(max_length=45, blank=True, null=True)
    empleado = models.ForeignKey('empleado', on_delete=models.DO_NOTHING, db_column='empleado_id', related_name='cuentas_bancarias')

    class Meta:
        db_table = 'cuenta_bancaria'
        managed = True


class turno(BaseModel):
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField()

    class Meta:
        db_table = 'turno'
        managed =  True

    # --------- agregado ---------
    def __str__(self):
        return f"{self.hora_entrada.strftime('%H:%M')}–{self.hora_salida.strftime('%H:%M')}"
    # ----------------------------


class jornada(BaseModel):
    nombre = models.CharField(max_length=45)
    horas_semanales = models.IntegerField()


    class Meta:
        db_table = 'jornada'
        managed = True

    # --------- agregado ---------
    def __str__(self):
        return f"{self.nombre} ({self.horas_semanales} h/sem)"
    # ----------------------------


class turno_has_jornada(BaseModel):
    turno = models.ForeignKey('turno', on_delete=models.DO_NOTHING, db_column='turno_id')
    jornada = models.ForeignKey('jornada', on_delete=models.DO_NOTHING, db_column='jornada_id')

    class Meta:
        db_table = 'turno_has_jornada'
        managed = True
        unique_together = (('turno', 'jornada'),)

    # --------- agregado ---------
    def __str__(self):
        # Se apoya en los __str__ de turno y jornada
        return f"{self.turno} / {self.jornada}"
    # ----------------------------


class contrato(BaseModel):
    # -----------------------------
    # Choices nuevos (para CRUD)
    # -----------------------------
    ESTADOS = [
        ("Vigente", "Vigente"),
        ("En firma", "En firma"),
        ("Finalizado", "Finalizado"),
    ]

    TIPOS = [
        ("Indefinido", "Indefinido"),
        ("Plazo fijo", "Plazo fijo"),
        ("Part-time", "Part-time"),
        ("Práctica", "Práctica"),
    ]

    # -----------------------------
    # Campos existentes (NO se tocan)
    # -----------------------------
    detalle_contrato = models.CharField(max_length=45, blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)

    empleado = models.ForeignKey(
        'empleado', on_delete=models.DO_NOTHING, db_column='empleado_id'
    )
    cargo = models.ForeignKey(
        'cargo', on_delete=models.DO_NOTHING, db_column='cargo_id'
    )
    departamento = models.ForeignKey(
        'departamento', on_delete=models.DO_NOTHING, db_column='departamento_id'
    )
    turno_has_jornada = models.ForeignKey(
        'turno_has_jornada',
        on_delete=models.DO_NOTHING,
        db_column='turno_has_jornada_id',
        null=True, blank=True,             # ← permitir nulos
    )

    # -----------------------------
    # Campos NUEVOS (no rompen nada)
    # -----------------------------
    tipo = models.CharField(max_length=40, choices=TIPOS, default="Indefinido")
    estado = models.CharField(max_length=20, choices=ESTADOS, default="Vigente")
    pdf = models.FileField(upload_to="contratos/", blank=True, null=True)

    class Meta:
        db_table = 'contrato'
        managed = True
        ordering = ['-fecha_inicio']
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"

    def __str__(self):
        # Se apoya en los __str__ de empleado y cargo
        return f"{self.empleado} — {self.cargo} ({self.tipo}, {self.estado})"

    @property
    def esta_vigente(self):
        return self.estado == "Vigente"

    @property
    def en_firma(self):
        return self.estado == "En firma"

    @property
    def finalizado(self):
        return self.estado == "Finalizado"


class liquidacion(BaseModel):
    periodo = models.DateField()
    fecha_pago = models.DateField(blank=True, null=True)

    imponible = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    no_imponible = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tributable = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    descuentos = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    anticipo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    liquido = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    devengado = models.DateField(blank=True, null=True)
    cierre = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=45)

    contrato = models.ForeignKey('contrato', on_delete=models.DO_NOTHING, db_column='contrato_id')

    class Meta:
        db_table = 'liquidacion'
        managed = True


class forma_pago(BaseModel):
    nombre = models.CharField(max_length=45)
    description = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'forma_pago'
        managed = True


class pago(BaseModel):
    fecha_pago = models.DateField()
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    comprobante = models.CharField(max_length=45, blank=True, null=True)
    estado = models.CharField(max_length=45)

    liquidacion = models.ForeignKey('liquidacion', on_delete=models.DO_NOTHING, db_column='liquidacion_id', related_name='pagos')
    forma_pago = models.ForeignKey('forma_pago', on_delete=models.DO_NOTHING, db_column='forma_pago_id')

    class Meta:
        db_table = 'pago'
        managed = True


class ZonaTrabajo(BaseModel):
    nombre = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    supervisor = models.CharField(max_length=100)
    notas = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'zona_trabajo'
        managed = True
        verbose_name = 'Zona de Trabajo'
        verbose_name_plural = 'Zonas de Trabajo'

    def __str__(self):
        return f"{self.nombre} - {self.area}"



class Foto(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='galeria/')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ['-fecha_subida']

    def __str__(self):
        return self.titulo
