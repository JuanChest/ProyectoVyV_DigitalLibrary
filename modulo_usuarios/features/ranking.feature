# language: es
# Created by Juan at 23/6/2026
Característica: Ranking público de los 10 estudiantes con mayor prestigio
  Como visitante de Notable
  Quiero ver un ranking con los 10 estudiantes más destacados
  Para conocer qué estudiantes generan el contenido más valioso en la comunidad

  Antecedentes:
    Dado que existen estudiantes registrados con apuntes publicados
    Y cada apunte ha recibido votos de la comunidad

  Regla: El ranking muestra exactamente los 10 estudiantes con mayor puntaje de prestigio

    Escenario: Visitante ve el ranking cuando hay 10 o más estudiantes con prestigio
      Dado que al menos 10 estudiantes tienen puntos de prestigio mayores a 0
      Cuando un visitante accede a la página de ranking
      Entonces ve exactamente 10 estudiantes listados
      Y están ordenados de mayor a menor puntaje de prestigio
      Y cada entrada muestra el nombre del estudiante, su rango y su puntaje

    Escenario: El ranking muestra menos de 10 si la comunidad es pequeña
      Dado que solo 3 estudiantes tienen puntos de prestigio mayores a 0
      Cuando un visitante accede a la página de ranking
      Entonces ve exactamente 3 estudiantes listados
      Y están ordenados de mayor a menor puntaje de prestigio

    Escenario: No se puede ver el ranking sin iniciar sesión
      Dado que el visitante no ha iniciado sesión
      Cuando accede directamente a la URL del ranking
      Entonces es redirigido a la página de login

  Regla: El rango de un estudiante refleja su puntaje acumulado de prestigio

    Esquema del escenario: El rango se asigna correctamente según el puntaje
      Dado que un estudiante tiene <puntaje> puntos de prestigio
      Cuando aparece en el ranking
      Entonces su rango visible es "<rango>"

      Ejemplos:
        | puntaje | rango     |
        | 0       | Prepo     |
        | 150     | Prepo     |
        | 299     | Prepo     |
        | 300     | Tecnólogo |
        | 500     | Tecnólogo |
        | 699     | Tecnólogo |
        | 700     | Ingeniero |
        | 1500    | Ingeniero |
        | 2999    | Ingeniero |
        | 3000    | PhD       |
        | 9999    | PhD       |