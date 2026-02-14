package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * SBOM Example Application
 * 
 * Spring Boot 기반 간단한 REST API 애플리케이션
 * SBOM 생성 테스트를 위한 예제입니다.
 */
@SpringBootApplication
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    @RestController
    public class HelloController {
        
        @GetMapping("/")
        public String hello() {
            return "SBOM Example Application is running!";
        }

        @GetMapping("/health")
        public String health() {
            return "OK";
        }
    }
}
