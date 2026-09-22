;;; Cobertura conceitual plana: cotas em mm, sem dimensionamento estrutural.
(defun cg:with-roof (model / outline b height w roof)
  (if (cg:get "error" model) model
    (progn
      (setq outline (cg:get "footprint" model))
      (if (not outline) (setq outline (cg:get "outline" (cg:get "slab" model))))
      (if (not outline)
        (progn (setq b (cg:get "house_bounds" model))
          (setq outline (list (list (nth 0 b) (nth 1 b)) (list (nth 2 b) (nth 1 b))
            (list (nth 2 b) (nth 3 b)) (list (nth 0 b) (nth 3 b))))))
      (setq height 0.0)
      (foreach w (cg:get "walls" model) (setq height (max height (cg:get "height" w))))
      (setq roof (list (cons "kind" "flat_slab") (cons "outline" outline)
        (cons "base_z" height) (cons "thickness" 150.0)
        (cons "parapet_height" 600.0) (cons "parapet_thickness" 100.0)
        (cons "note" "Cobertura conceitual: caimentos, drenagem, impermeabilizacao e estrutura a projetar.")))
      (if (assoc "roof" model) (subst (cons "roof" roof) (assoc "roof" model) model)
        (append model (list (cons "roof" roof)))))))
(princ)
