#lang racket

(provide color
         with-opacity)

;; Color helpers

(define-syntax color
  (syntax-rules ()
    [(color r g b) (vector r g b 1.0)]
    [(color r g b a) (vector r g b a)]))

(define (with-opacity color-vec opacity)
  (vector (vector-ref color-vec 0)
          (vector-ref color-vec 1)
          (vector-ref color-vec 2)
          opacity))