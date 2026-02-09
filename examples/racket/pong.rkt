#lang racket

(require gridcode/grid/main
         gridcode/gridcode)

(define display-name "Pong")
(define grid-size 32)
(define frame-rate 30)

(define (setup-grid)
  (define columns grid-size)
  (define rows grid-size)

  (for ([y (in-range rows)])
    (set-cell! 0 y "wall" #t)
    (set-cell! 0 y "dx" 1)
    (set-cell! (- columns 1) y "wall" #t)
    (set-cell! (- columns 1) y "dx" -1))

  (for ([x (in-range columns)])
    (set-cell! x 0 "wall" #t)
    (set-cell! x 0 "dy" 1)
    (set-cell! x (- rows 1) "out" #t))

  (define center (quotient rows 2))
  (define paddle-range (range (- center 2) (+ center 3)))
  (for ([x paddle-range])
    (set-cell! x (- rows 1) "paddle" #t))

  (define ball-x (list-ref paddle-range (random (length paddle-range))))
  (define dx (list-ref '(-1 1) (random 2)))
  (set-cell! ball-x (- rows 2) "ball" (list dx -1)))

(define (update-grid)
  (define ball-coords (get-all-xy "ball"))
  (when (not (empty? ball-coords))
    (define ball-pos (first ball-coords))
    (define ball-x (first ball-pos))
    (define ball-y (second ball-pos))
    (define ball-vel (get-cell ball-x ball-y "ball"))
    (define dx (first ball-vel))
    (define dy (second ball-vel))
    (define new-x (+ ball-x dx))
    (define new-y (+ ball-y dy))

    (delete-cell! ball-x ball-y "ball")

    (cond
      [(get-cell new-x new-y "wall")
       (define new-dx (get-cell new-x new-y "dx" dx))
       (define new-dy (get-cell new-x new-y "dy" dy))
       (set-cell! (+ ball-x new-dx) (+ ball-y new-dy) "ball" (list new-dx new-dy))]

      [(get-cell ball-x new-y "paddle")
       (define new-dx (list-ref '(-1 1) (random 2)))
       (set-cell! (+ ball-x new-dx) (- ball-y 1) "ball" (list new-dx -1))]

      [(get-cell new-x new-y "out")
       (set-cell! ball-x new-y "ball-out" (list 0 0))]

      [else
       (set-cell! new-x new-y "ball" (list dx dy))])))

(define (color-for-cell x y)
  (cond
    [(get-cell x y "wall") (color 1.0 1.0 1.0)]
    [(get-cell x y "ball-out") (color 1.0 0.0 0.0)]
    [(get-cell x y "ball") (color 0.2 0.9 0.0)]
    [(get-cell x y "paddle") (color 1.0 0.8 0.2)]
    [else (color 0.0 0.0 0.0)]))

(define (info-for-cell x y)
  (format "[~a|~a] ~a" x y (get-cell x y)))

(define (handle-cell-tapped x y)
  (define paddle-xs (map first (get-all-xy "paddle")))
  (define paddle-left-x (apply min paddle-xs))
  (define paddle-right-x (apply max paddle-xs))
  (define bottom-y (- grid-size 1))
  (define columns grid-size)

  (if (< x (quotient columns 2))
      (when (> paddle-left-x 1)
        (delete-cell! paddle-right-x bottom-y "paddle")
        (set-cell! (- paddle-left-x 1) bottom-y "paddle" #t))

      (when (< paddle-right-x (- columns 2))
        (delete-cell! paddle-left-x bottom-y "paddle")
        (set-cell! (+ paddle-right-x 1) bottom-y "paddle" #t))))

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