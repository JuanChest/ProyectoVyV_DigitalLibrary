# modulo_usuarios/features/steps/ranking_steps.py

from behave import given, when, then
from django.test import Client
from django.contrib.auth.models import User
from modulo_usuarios.models.perfil_estudiante import PerfilEstudiante


# ── HELPERS ───────────────────────────────────────────────────────────────────

def _crear_estudiante(username, puntos):
    """Crea un User + PerfilEstudiante con puntos dados. Idempotente por username."""
    user, _ = User.objects.get_or_create(username=username)
    user.set_password("test1234")
    user.save()
    perfil = user.perfil  # creado automáticamente por el signal
    perfil.puntos_prestigio = puntos
    perfil.save()
    return perfil


# ── BACKGROUND ────────────────────────────────────────────────────────────────

@given("que existen estudiantes registrados con apuntes publicados")
def step_estudiantes_con_apuntes(context):
    # El Background es declarativo; los datos concretos los crean los Given de cada escenario.
    pass

@given("cada apunte ha recibido votos de la comunidad")
def step_apuntes_con_votos(context):
    # Ídem: declarativo. Los escenarios de votos se cubrirán en features de interacciones.
    pass


# ── GIVEN ─────────────────────────────────────────────────────────────────────

@given("que al menos 10 estudiantes tienen puntos de prestigio mayores a 0")
def step_diez_estudiantes_con_prestigio(context):
    for i in range(1, 16):  # creamos 15 para probar que solo aparecen 10
        _crear_estudiante(f"estudiante_{i:02d}", puntos=i * 50)
    context.client = Client()

@given("que solo 3 estudiantes tienen puntos de prestigio mayores a 0")
def step_tres_estudiantes_con_prestigio(context):
    for i in range(1, 4):
        _crear_estudiante(f"menor_{i}", puntos=i * 100)
    context.client = Client()

@given("que el visitante no ha iniciado sesión")
def step_visitante_sin_login(context):
    context.client = Client()  # cliente sin autenticar

@given("que un estudiante tiene {puntaje:d} puntos de prestigio")
def step_estudiante_con_puntaje(context, puntaje):
    context.perfil = _crear_estudiante("estudiante_rango", puntos=puntaje)


# ── WHEN ──────────────────────────────────────────────────────────────────────

@when("un visitante accede a la página de ranking")
def step_acceder_ranking(context):
    context.response = context.client.get("/ranking/")

@when("accede directamente a la URL del ranking")
def step_acceder_url_ranking(context):
    context.response = context.client.get("/ranking/")

@when("aparece en el ranking")
def step_aparece_en_ranking(context):
    # Solo validamos la propiedad del modelo, no hace falta HTTP aquí
    pass


# ── THEN ──────────────────────────────────────────────────────────────────────

@then("ve exactamente {cantidad:d} estudiantes listados")
def step_cantidad_estudiantes(context, cantidad):
    top = context.response.context["top_publicadores"]
    assert len(top) == cantidad, (
        f"Se esperaban {cantidad} estudiantes, se obtuvieron {len(top)}"
    )

@then("están ordenados de mayor a menor puntaje de prestigio")
def step_ordenados_por_prestigio(context):
    top = context.response.context["top_publicadores"]
    puntajes = [p.puntos_prestigio for p in top]
    assert puntajes == sorted(puntajes, reverse=True), (
        f"El ranking no está ordenado correctamente: {puntajes}"
    )

@then("cada entrada muestra el nombre del estudiante, su rango y su puntaje")
def step_datos_completos(context):
    top = context.response.context["top_publicadores"]
    for perfil in top:
        assert perfil.usuario.username, "Falta el nombre de usuario"
        assert perfil.rango in ("Prepo", "Tecnólogo", "Ingeniero", "PhD"), (
            f"Rango inválido: {perfil.rango}"
        )
        assert isinstance(perfil.puntos_prestigio, int), "Faltan los puntos"

@then("puede ver el ranking sin ser redirigido al login")
def step_sin_redireccion_login(context):
    assert context.response.status_code == 200, (
        f"Se esperaba 200, se obtuvo {context.response.status_code}. "
        "Posiblemente hay un login_required en la vista."
    )

@then('su rango visible es "{rango}"')
def step_rango_correcto(context, rango):
    assert context.perfil.rango == rango, (
        f"Con {context.perfil.puntos_prestigio} pts se esperaba '{rango}', "
        f"pero se obtuvo '{context.perfil.rango}'"
    )