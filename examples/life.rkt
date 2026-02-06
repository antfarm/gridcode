#lang gridcode

(define neighborhood
  '((-1 -1) (0 -1) (1 -1) (-1  0) (1  0) (-1  1) (0  1) (1  1)))

(define size 64)

(define (neighbors-alive-count x y)
  (define neighbors
    (map (lambda (offset)
           (define dx (first offset))
           (define dy (second offset))
           (list (modulo (+ x dx) size)
                 (modulo (+ y dy) size)))
         neighborhood))
  (length (filter (lambda (coord)
                    (define nx (first coord))
                    (define ny (second coord))
                    (equal? "alive" (get-cell nx ny "state")))
                  neighbors)))

(define color-alive (color 1.0 0.8 0.2))
(define color-dead (color 0.0 0.0 0.0))

(define my-program
  (hash 'grid-size size
        'frame-rate 60

        'setup-grid
        (lambda ()
          (define percent-alive 20)
          (for* ([x (in-range size)]
                 [y (in-range size)])
            (define is-alive (< (random 100) percent-alive))
            (set-cell! x y "state" (if is-alive "alive" "dead"))
            (set-cell! x y "age" (if is-alive 1 0))))

        'update-grid
        (lambda ()
          ;; Count neighbors
          (for* ([x (in-range size)]
                 [y (in-range size)])
            (set-cell! x y "count" (neighbors-alive-count x y)))

          ;; Update based on rules
          (for* ([x (in-range size)]
                 [y (in-range size)])
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

        'color-for-cell
        (lambda (x y)
          (define state (get-cell x y "state"))
          (define age (get-cell x y "age" 0))
          (define opacity (/ (- 10 (min age 6)) 10.0))
          (if (equal? state "alive")
              (with-opacity color-alive opacity)
              color-dead))

        'info-for-cell
        (lambda (x y)
          (format "[~a|~a] ~a" x y (get-cell x y)))

        'handle-cell-tapped
        (lambda (x y)
          (define state (get-cell x y "state"))
          (set-cell! x y "state" (if (equal? state "alive") "dead" "alive"))
          (set-cell! x y "age" (if (equal? state "alive") 0 1)))))

(void (run my-program))