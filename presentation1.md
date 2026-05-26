---
marp: true
theme: gaia
# Встраиваем свой CSS прямо в директивы
style: |
  .columns {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
  }
---

# Слайд с двумя колонками

<div class="columns">
<div>

## Колонка 1
- Содержимое первой колонки
- `code example`
- Текст...

</div>
<div>

## Колонка 2
- Содержимое второй колонки
- ![width:200px](https://marp.app/assets/marp.svg)

</div>
</div>
