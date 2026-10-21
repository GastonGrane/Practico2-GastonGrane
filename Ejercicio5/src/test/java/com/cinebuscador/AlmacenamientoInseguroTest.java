package com.cinebuscador;

import static org.junit.jupiter.api.Assertions.assertNotEquals;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.ui.ConcurrentModel;

import com.cinebuscador.controller.AuthController;
import com.cinebuscador.model.User;
import com.cinebuscador.repository.UserRepository;

// esta prueba usa @SpringBootTest, levanta el contexto de spring entero (igual que si corriera la app), pero sin
// necesidad de docker ni de un servidor http real: se llama directo al metodo register del controller, como una llamada normal de java
@SpringBootTest
class AlmacenamientoInseguroTest {

    @Autowired
    private AuthController authController;

    @Autowired
    private UserRepository userRepository;

    @Test
    void mismaPasswordNoQuedaGuardadaIgual() {
        // registro dos usuarios distintos con la misma contraseña, exactamente lo mismo que probe a mano
        // desde el navegador en el practico 2
        authController.register("usuarioTest1", "MismaClave123", "MismaClave123", new ConcurrentModel());
        authController.register("usuarioTest2", "MismaClave123", "MismaClave123", new ConcurrentModel());

        // leo de la base de datos como quedo guardada la contraseña de cada uno de los dos usuarios
        User usuario1 = userRepository.findByUsername("usuarioTest1").orElseThrow();
        User usuario2 = userRepository.findByUsername("usuarioTest2").orElseThrow();

        // si la app sigue vulnerable (cifrado AES en modo ECB, deterministico), la misma contraseña siempre da el mismo resultado cifrado, entonces 
        // las dos quedan IGUALES. si ya esta mitigada (bcrypt, que usa un salt aleatorio distinto cada vez), las dos quedan 
        // DISTINTAS aunque la contraseña en texto plano sea la misma.
        assertNotEquals(usuario1.getPassword(), usuario2.getPassword());
    }
}