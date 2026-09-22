casa_form : dialog {
 label = "CASA BH - estudo preliminar 0.4";
 : text { label = "Casa terrea | terreno hipotetico plano | medidas em metros"; }
 : row {
  : boxed_column { label = "Terreno e construcao";
   : edit_box { key = "lot_width"; label = "Largura lote"; edit_width = 10; }
   : edit_box { key = "lot_depth"; label = "Profundidade lote"; edit_width = 10; }
   : edit_box { key = "house_width"; label = "Largura casa"; edit_width = 10; }
   : edit_box { key = "wall_internal"; label = "Parede interna"; edit_width = 10; }
   : edit_box { key = "wall_external"; label = "Parede externa"; edit_width = 10; }
   : edit_box { key = "height"; label = "Pe-direito"; edit_width = 10; }
   : edit_box { key = "corridor"; label = "Largura corredor"; edit_width = 10; }
  }
  : boxed_column { label = "Ambientes (quantidades obrigatorias)";
   : edit_box { key = "bedrooms"; label = "Quartos"; edit_width = 6; }
   : edit_box { key = "bathrooms"; label = "Banheiros sociais"; edit_width = 6; }
   : edit_box { key = "living"; label = "Salas de estar"; edit_width = 6; }
   : edit_box { key = "kitchens"; label = "Cozinhas"; edit_width = 6; }
   : edit_box { key = "laundry"; label = "Lavanderias"; edit_width = 6; }
   : edit_box { key = "dining"; label = "Salas de jantar"; edit_width = 6; }
   : edit_box { key = "office"; label = "Escritorios"; edit_width = 6; }
  }
 }
 : boxed_row { label = "Faixas livres de ENSAIO - nao sao recuos legais de BH";
  : edit_box { key = "front"; label = "Frente"; edit_width = 7; }
  : edit_box { key = "rear"; label = "Fundos"; edit_width = 7; }
  : edit_box { key = "side"; label = "Laterais"; edit_width = 7; }
 }
 : row {
  : edit_box { key = "seed"; label = "Semente da alternativa"; edit_width = 12; }
  : toggle { key = "furniture"; label = "Inserir mobiliario esquematico"; }
 }
 : boxed_row { label = "Moradores e alternativas";
  : edit_box { key = "occupants"; label = "Moradores (1-6)"; edit_width = 4; }
  : edit_box { key = "parking"; label = "Vagas (0-2)"; edit_width = 4; }
  : edit_box { key = "north"; label = "Norte em graus (0=+Y)"; edit_width = 5; }
 }
 : row {
  : popup_list { key = "layout"; label = "Organizacao"; width = 27; }
  : popup_list { key = "integration"; label = "Integracao social"; width = 24; }
  : toggle { key = "terrace"; label = "Convivencia externa"; }
 }
 : text { label = "Garagem descoberta; norte informado/hipotetico. Laje conceitual com platibanda; sem suites."; }
 : text { label = "Edicoes manuais CAD nao sao sincronizadas. Desempenho ambiental nao simulado."; }
 : text { label = "Com vaga: frente efetiva de ao menos 6.50 m para carro e acesso pedestre."; }
 : text { key = "error"; label = ""; width = 95; }
 ok_cancel;
}
