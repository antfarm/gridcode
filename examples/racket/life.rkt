#lang racket

(require gridcode/grid/main
         gridcode/gridcode)

(define display-name "Game of Life")
(define grid-size 64)
(define frame-rate 60)

(define neighborhood
  '((-1 -1) (0 -1) (1 -1) (-1  0) (1  0) (-1  1) (0  1) (1  1)))

(define (neighbors-alive-count x y)
  (define neighbors
    (map (lambda (offset)
           (define dx (first offset))
           (define dy (second offset))
           (list (modulo (+ x dx) grid-size)
                 (modulo (+ y dy) grid-size)))
         neighborhood))

  (length (filter (lambda (coord)
                    (define nx (first coord))
                    (define ny (second coord))
                    (equal? "alive" (get-cell nx ny "state")))
                  neighbors)))

(define (setup-grid)
  (define percent-alive 20)
  (for* ([x (in-range grid-size)]
         [y (in-range grid-size)])
    (define is-alive (< (random 100) percent-alive))
    (set-cell! x y "state" (if is-alive "alive" "dead"))
    (set-cell! x y "age" (if is-alive 1 0))))

(define (update-grid)
  (for* ([x (in-range grid-size)]
         [y (in-range grid-size)])
    (set-cell! x y "count" (neighbors-alive-count x y)))

  (for* ([x (in-range grid-size)]
         [y (in-range grid-size)])
    (define state (get-cell x y "state"))
    (define count (get-cell x y "count"))
    (define age (get-cell x y "age"))
    (if (equal? state "alive")
        (if (or (= count 2) (= count 3))
            (set-cell! x y "age" (+ age 1))  ; survival
            (begin  ; death
              (set-cell! x y "state" "dead")
              (set-cell! x y "age" 0)))
        (when (= count 3)  ; birth
          (set-cell! x y "state" "alive")
          (set-cell! x y "age" 1)))))

(define (color-for-cell x y)
  (define state (get-cell x y "state"))
  (define age (get-cell x y "age" 0))
  (define opacity (/ (- 10 (min age 6)) 10.0))
  (if (equal? state "alive")
      (with-opacity (color 1.0 0.8 0.2) opacity)
      (color 0.0 0.0 0.0)))

(define (info-for-cell x y)
  (format "[~a|~a] ~a" x y (get-cell x y)))

(define (handle-cell-tapped x y)
  (define state (get-cell x y "state"))
  (set-cell! x y "state" (if (equal? state "alive") "dead" "alive"))
  (set-cell! x y "age" (if (equal? state "alive") 0 1)))

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