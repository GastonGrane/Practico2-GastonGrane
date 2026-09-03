package com.cinebuscador.controller;

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.cinebuscador.model.Funcion;
import com.cinebuscador.repository.FuncionRepository;

@Controller
public class FuncionController {

    private final FuncionRepository funcionRepo;

    @Autowired
    public FuncionController(FuncionRepository funcionRepo) {
        this.funcionRepo = funcionRepo;
    }

    @GetMapping("/")
    public String search(@RequestParam(required = false) String buscar, Model model) {

        model.addAttribute("query", buscar != null ? buscar : "");

        if (buscar == null || buscar.isBlank()) {
            System.out.println("buscar es: " + buscar);
            // Mostrar todas las funciones si no hay busqueda
            List<Funcion> todas = funcionRepo.findAll();
            model.addAttribute("resultados", todas);
            model.addAttribute("mensaje", "Mostrando todas las funciones.");
            return "index";
        }

          List<Funcion> resultados = funcionRepo.findAll().stream()
            .filter(f -> f.getNombreFuncion() != null &&
                         f.getNombreFuncion().toLowerCase().contains(buscar.toLowerCase()))
            .collect(Collectors.toList());
        model.addAttribute("resultados", resultados);
        model.addAttribute("mensaje", "Resultados buscando por: " + buscar);

        return "index";
    }
}
