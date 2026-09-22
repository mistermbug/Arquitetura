(defun fr:check (condition label)
  (if (not condition) (setq failures (1+ failures)))
  (write-line (strcat (if condition "PASS " "FAIL ") label) fh))
(defun fr:run (path / fh failures zone model items again rotations seed it ln pt box mirrors)
  (setq fh (open path "w") failures 0 rotations nil mirrors nil seed 1
    zone '(("id" . "Z1") ("kind" . "bedroom") ("bounds" 1000 2000 5000 6000)))
  (repeat 32
    (setq model (list (cons "seed" seed)) items (cf:place zone model T) again (cf:place zone model T))
    (fr:check (and items (equal items again 0.0001)) (strcat "REPRODUCIBLE " (itoa seed)))
    (if (not (member (cg:get "rotation" (car items)) rotations)) (setq rotations (cons (cg:get "rotation" (car items)) rotations)))
    (if (not (member (cg:get "mirror" (car items)) mirrors)) (setq mirrors (cons (cg:get "mirror" (car items)) mirrors)))
    (foreach it items
      (setq box (cg:get "bounds" it))
      (foreach ln (cg:get "symbol_lines" it)
        (foreach pt ln
          (fr:check (cf:inside (list (car pt) (cadr pt) (car pt) (cadr pt)) box) "SYMBOL_INSIDE_TRANSFORMED_FOOTPRINT"))))
    (fr:check (cf:valid items (cg:get "bounds" zone) nil) "CLEARANCE")
    (setq seed (1+ seed)))
  (fr:check (= (length rotations) 4) (strcat "ALL_FOUR_ROTATIONS " (vl-princ-to-string rotations)))
  (fr:check (= (length mirrors) 2) "BOTH_MIRRORS")
  (write-line (strcat "COMPLETE failures=" (itoa failures)) fh)
  (close fh) (princ))
