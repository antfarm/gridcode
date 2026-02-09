#lang racket

(require gridcode/grid/main
         gridcode/gridcode)

(define display-name "Hello")
(define grid-size 16)
(define frame-rate 2)

(define (setup-grid)
  (for ([x (in-range 16)])
    (set-cell! x x "alive" #t)))

(define (update-grid)
  (for* ([x (in-range 16)]
         [y (in-range 16)])
    (define alive (get-cell x y "alive"))
    (set-cell! x y "alive" (not alive))))

(define (color-for-cell x y)
  (if (get-cell x y "alive")
      (color 1.0 0.8 0.2)
      (color 0.0 0.0 0.0)))

(define (info-for-cell x y)
  (format "[~a|~a] alive: ~a" x y (get-cell x y "alive")))

(define (handle-cell-tapped x y)
  (define alive (get-cell x y "alive"))
  (set-cell! x y "alive" (not alive)))

(define program
  (hash 'display-name display-name
        'grid-size grid-size
        'frame-rate frame-rate
        'setup-grid setup-grid
        'update-grid update-grid
        'color-for-cell color-for-cell
        'info-for-cell info-for-cell
        'handle-cell-tapped handle-cell-tapped))

(run program)