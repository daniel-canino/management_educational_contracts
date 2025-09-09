# Gestión de Contratos Educativos

Este módulo de Odoo facilita la administración de contratos educativos y la gestión de asignaturas y dashboards asociados.

## Características

- **Gestión de Contratos:** Crear, editar y visualizar contratos educativos.  
- **Dashboard Educativo:** Visualización de información resumida e indicadores clave.  
- **Gestión de Asignaturas:** Administración de las materias vinculadas a los contratos.  
- **Integración Contable:** Interfaz con [account_move](models/account_move.py) para la gestión de facturación.  
- **Seguridad:** Configuración de permisos definida en [ir.model.access.csv](security/ir.model.access.csv).

## Estructura del Módulo

- **controllers/**  
  Contiene controladores web para el dashboard y otras interfaces. Ejemplo: [dashboard_controller.py](controllers/dashboard_controller.py).
- **data/**  
  Archivos de datos iniciales, como secuencias (por ejemplo, [ir_sequence.xml](data/ir_sequence.xml)).
- **models/**  
  Definición de modelos de datos, incluyendo contratos, asignaturas y movimientos contables.  
- **static/**  
  Recursos estáticos y descripciones.
- **views/**  
  Vistas definidas en XML para la interfaz de usuario, incluyendo formularios y paneles (como [educational_contract_views.xml](views/educational_contract_views.xml)).