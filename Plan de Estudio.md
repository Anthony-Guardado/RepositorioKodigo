# Plan de Estudio del Proyecto CliniCore

## 1. Configuración Global y Raíz

Aquí vive el punto de entrada de la aplicación, la configuración de Android y los archivos de Gradle.

- `MainActivity.kt`
    
- `CliniCoreApplication.kt`
    
- `AndroidManifest.xml`
    
- `build.gradle.kts` (Módulo app)
    
- `build.gradle.kts` (Raíz)
    
- `libs.versions.toml`
    

## 2. Paquete `data`

Contiene los modelos de datos puros (DTOs) que viajan entre la app y la API, los modelos locales, la configuración de DataStore para la sesión y las utilidades de soporte.

- `UsuarioDto.kt`
    
- `AuthDto.kt`
    
- `PerfilDto.kt`
    
- `EspecialidadDto.kt`
    
- `Sesion.kt`
    
- `SesionDataStore.kt`
    

## 3. Paquete `data.remote`

Se encarga exclusivamente de la comunicación con el exterior (Internet). Aquí viven las interfaces de Retrofit que definen las rutas de tu API y los interceptores de red.

- `ApiConfig.kt`
    
- `AuthApi.kt`
    
- `UsuarioApi.kt`
    
- `PerfilApi.kt`
    
- `EspecialidadApi.kt`
    
- `AuthInterceptor.kt`
    

## 4. Paquete `repository`

Es la capa intermedia entre los ViewModels y las fuentes de datos (Retrofit/DataStore). Su trabajo es pedir los datos, manejar los posibles errores (como los HTTP 409) y entregar un resultado limpio.

- `AuthRepository.kt`
    
- `UsuarioRepository.kt`
    
- `PerfilRepository.kt`
    
- `EspecialidadRepository.kt`
    
- `SesionRepository.kt`
    

## 5. Paquete `di` (Dependency Injection)

Contiene las "recetas" de Hilt. Aquí se le enseña al sistema cómo construir Retrofit, el cliente OkHttp (con su interceptor JWT) y cómo conectar todas las APIs.

- `NetworkModule.kt`
    

## 6. Paquete `viewmodel`

Contiene la lógica de negocio y el estado de la UI. Aquí se gestionan las corrutinas, las validaciones y se sobrevive a la rotación de pantalla sin perder los datos.

- `SesionViewModel.kt`
    
- `UsuariosViewModel.kt`
    
- `PerfilViewModel.kt`
    
- `EspecialidadViewModel.kt`
    

## 7. Paquete `navigation`

Gestiona el flujo de pantallas. Decide si mostrar el Login o la App (Lista/Perfil/Registro) basándose en el estado de la sesión.

- `NavManager.kt`
    

## 8. Paquete `ui` (Interfaz de Usuario)

Todo lo visual hecho en Jetpack Compose.

- `ui/theme/`: `Color.kt`, `Theme.kt`, `Type.kt`
    
- `ui/views/`:
    
    - `LoginView.kt`
        
    - `ListaUsuariosView.kt`
        
    - `PerfilView.kt`
        
    - `RegistroUsuarioView.kt`
        

## 9. Utilidades

Funciones auxiliares que no dependen de la interfaz ni de la base de datos.

- `utils/JwtUtil.kt`
    

---

## 10. Dependencias del Proyecto

Estas son las librerías base que hacen funcionar toda la arquitectura de CliniCore.

**Jetpack Compose:**

- `androidx.compose.bom`
    
- `androidx.compose.ui`, `ui-graphics`, `ui-tooling-preview`
    
- `androidx.compose.material3`
    

**Inyección de Dependencias (Hilt):**

- `com.google.dagger:hilt-android`
    
- `com.google.dagger:hilt-android-compiler` (con KSP)
    
- `androidx.hilt:hilt-navigation-compose`
    

**Red (Retrofit + OkHttp):**

- `com.squareup.retrofit2:retrofit`
    
- `com.squareup.retrofit2:converter-gson`
    
- `com.squareup.okhttp3:logging-interceptor`
    

**Persistencia y Utilidades:**

- `androidx.datastore:datastore-preferences`
    
- `androidx.lifecycle:lifecycle-viewmodel-compose`
    
- `androidx.lifecycle:lifecycle-runtime-compose`
