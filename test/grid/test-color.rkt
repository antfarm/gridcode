#lang racket

(require rackunit
         gridcode/grid/color)

(test-case "color macro - RGB"
           (check-equal? (color 1.0 0.5 0.2) #(1.0 0.5 0.2 1.0)))

(test-case "color macro - RGBA"
           (check-equal? (color 1.0 0.5 0.2 0.8) #(1.0 0.5 0.2 0.8)))

(test-case "with-opacity modifies alpha"
           (define blue (color 0.0 0.0 1.0))
           (check-equal? (with-opacity blue 0.5) #(0.0 0.0 1.0 0.5)))