### data/remote
- AuthApi:
	- Es en el cual construimos la ruta de los metodos agregando la anotacion de cada metodo. 
- AuthDto:
	-  Su único trabajo es ser el molde para que **Gson** (la librería de Retrofit) pueda convertir el texto JSON que viene de Spring Boot a objetos de Kotlin, y viceversa.
- AuthInterceptor:
	- Si `AuthApi` es el menú y `AuthDto` es el traductor, el **`AuthInterceptor` es el "guardaespaldas"** o el "sello de aprobación" que revisa cada petición antes de que salga a internet. 
- UsuarioApi:
	- Esta es la ruta para traer la lista de todos los usuarios.
### data
- Sesion: 
	- Cuando el usuario hace login y el backend le responde con el token, toda esa información se guarda temporalmente en la memoria del celular usando este modelo.
- SesionDataStore:
	- Si `Sesion.kt` era el "carnet de identidad" (el molde), `SesionDataStore.kt` es la **"caja fuerte física"** donde guardamos ese carnet en el teléfono para que no se pierda cuando cierres la app.
### di 
- NetworkModule:
	- **Qué hace:** Prepara todo. Toma el motor (`OkHttpClient`), le inyecta el guardaespaldas (`AuthInterceptor`), le dice a Retrofit cuál es la dirección de la empresa (`ApiConfig.BASE_URL`) y le dice: _"Usa Gson para traducir los datos"_.
	- **Su resultado:** Entrega "Retrofit" ya listo para usarse.
	- **Analogía:** Es el mecánico que arma el carro (Retrofit), le pone el motor (OkHttp) y le instala el GPS (ApiConfig).
 - Retrofit (El Traductor y Mensajero):
	- **Qué hace:** Toma tus interfaces (`AuthApi`, `UsuarioApi`) y las convierte en **peticiones HTTP reales**. Traduce tus objetos Kotlin a JSON y el JSON de vuelta a Kotlin.
	- **Su resultado:** Hace el viaje a internet y te trae la respuesta.
	- **Analogía:** Es el carro armado que maneja por la carretera.
### navigation
- NavManager (El Enrutador):  
	- Se encarga de manejar la **navegación (routing)** de la app. Decide qué pantalla mostrar basándose en el estado de la sesión (Login vs App) y en qué pantalla interna estamos (Lista, Perfil o Registro).
	- Gracias a esto, nos quitamos toda la lógica de navegación de `MainActivity`, dejándola limpia. El `MainActivity` solo crea los **ViewModels** y se los pasa al `NavManager` para que él se encargue de dibujar las pantallas correspondientes.
### repository 
- Es el que se encarga manipular los datos que necesita el viewmodel con los dtos manejando los errores **HTTP** y los metodos de cada proceso.
### ui/views
- Es donde creamos el diseño de los componentes que mandamos a llamar en el **viewmodel**.
### utils 
- JwtUtil:
	- Lee la fecha de vencimiento del token sin preguntarle al servidor.
### viewmodel
- Contiene la lógica de negocio y el estado de la UI. Aquí se gestionan las corrutinas, las validaciones y se sobrevive a la rotación de pantalla sin perder los datos.
