#lang racket

(provide init!
         set-cell!
         get-cell
         delete-cell!
         set-grid!
         get-grid
         delete-grid!
         get-all-xy
         delete-all!
         clear!)

;; Internal grid state

(define grid (make-hash))

(define (init! size)
  (set! grid (make-hash))
  (hash-set! grid 'cells (make-hash))
  (hash-set! grid 'data (make-hash))
  (hash-set! grid 'size size)
  (hash-set! grid 'coordinates
             (for*/list ([x (in-range size)]
                         [y (in-range size)])
               (list x y))))

;; Cell data

(define (set-cell! x y key [value #t])
  (let* ([cells (hash-ref grid 'cells)]
         [cell (hash-ref cells (list x y) (make-hash))])
    (hash-set! cell key value)
    (hash-set! cells (list x y) cell)))

(define get-cell
  (case-lambda
    [(x y)
     (let ([cells (hash-ref grid 'cells)])
       (hash-ref cells (list x y) (make-hash)))]
    [(x y key)
     (let* ([cells (hash-ref grid 'cells)]
            [cell (hash-ref cells (list x y) (make-hash))])
       (hash-ref cell key #f))]
    [(x y key default)
     (let* ([cells (hash-ref grid 'cells)]
            [cell (hash-ref cells (list x y) (make-hash))])
       (hash-ref cell key default))]))

(define (delete-cell! x y key)
  (let* ([cells (hash-ref grid 'cells)]
         [cell (hash-ref cells (list x y) #f)])
    (when cell
      (hash-remove! cell key))))

;; Grid data

(define (set-grid! key value)
  (let ([data (hash-ref grid 'data)])
    (hash-set! data key value)))

(define get-grid
  (case-lambda
    [(key)
     (let ([data (hash-ref grid 'data)])
       (hash-ref data key #f))]
    [(key default)
     (let ([data (hash-ref grid 'data)])
       (hash-ref data key default))]))

(define (delete-grid! key)
  (let ([data (hash-ref grid 'data)])
    (hash-remove! data key)))

;; Global operations

(define (all-coordinates)
  (hash-ref grid 'coordinates))

(define (get-all-xy key)
  (filter (lambda (coord)
            (let ([x (first coord)]
                  [y (second coord)])
              (get-cell x y key)))
          (all-coordinates)))

(define (delete-all! key)
  (for ([coord (all-coordinates)])
    (let ([x (first coord)]
          [y (second coord)])
      (delete-cell! x y key))))

(define clear!
  (case-lambda
    [()
     (hash-set! grid 'cells (make-hash))
     (hash-set! grid 'data (make-hash))]
    [(keys)
     (for ([k keys])
       (delete-all! k))]))