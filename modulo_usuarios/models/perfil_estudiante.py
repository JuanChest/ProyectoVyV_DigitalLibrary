from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class PerfilEstudiante(models.Model):
    # La relación estricta: un Perfil por cada Usuario de Django
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')

    # Atributos específicos para la plataforma de apuntes
    carrera = models.CharField(max_length=100, verbose_name="Carrera Universitaria")
    semestre_actual = models.IntegerField(default=1)
    foto_perfil = models.ImageField(upload_to='perfiles/avatares/', default='perfiles/default.png')

    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción Corta")
    bio = models.TextField(blank=True, null=True, verbose_name="Biografía o Información")
    temas_interes = models.CharField(max_length=255, blank=True, null=True, verbose_name="Temas de Interés")
    ira = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name="IRA")
    email_contacto = models.EmailField(blank=True, null=True, verbose_name="Email de Contacto")
    puntos_prestigio = models.IntegerField(default=0, verbose_name="Puntos de Prestigio")

    @property
    def rango(self):
        """
        Regla de negocio CP02: el rango se deriva exclusivamente del puntaje.
        Fuente única de verdad: puntos_prestigio.
        """
        if self.puntos_prestigio >= 3000:
            return "PhD"
        elif self.puntos_prestigio >= 700:
            return "Ingeniero"
        elif self.puntos_prestigio >= 300:
            return "Tecnólogo"
        return "Prepo"

    seguidores = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='siguiendo',
        blank=True,
        verbose_name="Seguidores"
    )

    @property
    def total_apuntes(self):
        """
        Cuenta los apuntes publicados por este estudiante.
        Requiere que el modelo Apunte tenga: autor = FK(PerfilEstudiante)
        Si el related_name es distinto, ajusta 'apuntes' aquí.
        """
        return self.apuntes.count()

    def __str__(self):
        return f"{self.usuario.username} [{self.rango}] — {self.puntos_prestigio} pts"

# SIGNAL: Crear perfil automáticamente
@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """
    Esta función se ejecuta automáticamente después de guardar un User.
    Evita colisiones con el panel de administración usando get_or_create.
    """
    if created:
        # get_or_create busca si ya existe un perfil asociado al usuario;
        # si ya existe (creado por el admin inline), no hace nada. Si no, lo crea de forma segura.
        PerfilEstudiante.objects.get_or_create(
            usuario=instance,
            defaults={
                'carrera': "No especificada",
                'semestre_actual': 1,
            }
        )

@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    """
    Esta función asegura que el perfil se guarde cuando el usuario se guarda.
    """
    # Solo ejecutar si el usuario tiene perfil (evita errores)
    if hasattr(instance, 'perfil'):
        instance.perfil.save()