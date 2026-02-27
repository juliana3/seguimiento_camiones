Intento de refactorización de Basurapp: 
[Proyecto original](https://github.com/juliana3/proyecto_final)

  Este proyecto consiste en el desarrollo de una API backend para gestionar y estimar el estado de la recolección domiciliaria de 
residuos según la ubicación del usuario. A partir de coordenadas geográficas (latitud y longitud), el sistema determina 
si existe recolección en la zona, si el servicio ya pasó, está en curso o aún no comenzó, y calcula una estimación del tiempo restante 
utilizando lógica temporal y consultas espaciales con PostGIS sobre rutas y zonas definidas. 
  Además, permite registrar reportes georreferenciados y gestionar notificaciones para usuarios autenticados, integrando 
autenticación con JWT y control de roles. 
  El objetivo es ofrecer una solución técnica que ayude a reducir la acumulación de residuos en la vía pública 
mediante información precisa y contextualizada.
