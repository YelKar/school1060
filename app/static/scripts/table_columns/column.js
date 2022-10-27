function column(col_id) {
    let col = document.createElement("div")
    col.classList.add("btn_block")
    col.classList.add("table_column")
    col.id = col_id

    let input = document.createElement("input")
    let label = document.createElement("label")
    input.type = "text"
    input.placeholder = "Заголовок"
    input.id = label.for = col_id
    label.hidden = true

    input.classList.add("column_header")
    let del_btn = document.createElement("button")
    del_btn.name = col_id
    del_btn.classList.add("del_btn")
    del_btn.textContent = "-"
    del_btn.style.fontWeight = "bold"
    del_btn.style.fontSize = "35px"
    del_btn.style.lineHeight = "5px"
    del_btn.style.paddingTop = "5px"
    del_btn.onclick = () => {
        main_block.removeChild(col)
        return false
    }

    col.appendChild(label)
    col.appendChild(input)
    col.appendChild(createSelect(col_id))
    col.appendChild(del_btn)
    return col
}

function createSelect(col_id) {
    let select = document.createElement("select")
    let not_fill = document.createElement("option")
    select.id = `select${col_id}`
    select.classList.add("column_fill")
    not_fill.textContent = "Не заполнять"
    not_fill.selected = true
    select.appendChild(not_fill)
    let fills = [
        ["name", "Имя"],
        ["lastname", "Фамилия"],
        ["patronymic", "Отчество"],
        ["classroom", "Класс"],
        ["classroom_and_letter", "Класс с буквой"],
        ["classroom_letter", "Буква класса"],
    ]
    for (let fill of fills) {
        let option = document.createElement("option")
        option.textContent = fill[1]
        option.value = fill[0]
        select.appendChild(option)
    }
    return select;
}

let main_block = document.querySelector("div.main_block")
let adding_column = document.querySelector("button#add_column")
let last_block = document.querySelector("div.add_column")
let columns = 0
adding_column.addEventListener("click", (e) => {
    main_block.insertBefore(column(++columns), last_block)
})

let del_btns = document.querySelectorAll("button.del_btn")

for (let del_btn of del_btns) {
    del_btn.addEventListener("click", (e) => {
        console.log(this.name)
    })
}
