/**
 * Script for checkboxes in details
 */

const details_all = document.querySelectorAll(" details") //

function all_checked(list) {
    for (let el of list) {
        if (el.id != "check" && !el.checked) return false
    }
    return true
}

for (let det of details_all) {
    let summary_input = det.querySelector("summary input");
    summary_input.addEventListener("change", (e) => {
        for (let input of det.querySelectorAll("input")) {
            input.checked = det.querySelector("summary input").checked;
        }
    })

    det.addEventListener("click", (e) => {
        setTimeout(() => {
            if (e.target != summary_input
                && all_checked(det.querySelectorAll("input")) != summary_input.checked) {
                summary_input.checked = all_checked(det.querySelectorAll("input"));
            }
        }, 10)
    })
}

// function get_selected() {
//     let classes = document.querySelectorAll(".chose_class")
//     let classes_let;
//     let checked = []
//     let students;
//     for (let classroom of classes) {
//         if (!classroom.checked) {
//             classes_let = document.querySelectorAll(`details details input.chose_class_let`)
//             console.log(classes_let)
//             for (let classroom_let of classes_let) {
//                 if (!classroom_let.checked) {
//
//                 } else {
//                     checked.push(classroom_let.id)
//                 }
//                 console.log(!classroom_let.checked)
//             }
//         } else {
//             checked.push(classroom.id)
//         }
//     }
//     return checked
// }


function to_generate(type) {
    let action_type = this.name
    let selected = get_selected()
    if (!selected.length) {
        return;
    }
    let doc_name = document.querySelector("#doc_name").value
    const link = document.createElement("a")
    link.href = "/generating_" + action_type
    let args = selected.join("&students=")
    args = `?type=${action_type}&doc=${doc_name}&students=${args}`
    link.href += args
    if (action_type == "xlsx") {
        const class_sheets = document.querySelector("input#class_sheet").checked
        const split_fullname = document.querySelector("input#split_fullname").checked
        link.href += `&class_sheets=${+class_sheets}
                      &split_fullname=${+split_fullname}`
    }
    let adding_column = document.querySelector("div.add_column")
    console.log(!!adding_column)
    if (adding_column) {
        let fills = document.querySelectorAll(".column_fill")
        let headers = document.querySelectorAll(".column_header")
        let table_args = ""
        for (let header of headers) {
            let head_value = header.value
            table_args += "&headers=" + head_value
        }
        for (let fill of fills) {
            let head_value = fill.value
            table_args += "&fills=" + head_value
        }
        link.href += table_args
    }
    link.click()
}

function get_selected() {
    let students = document.querySelectorAll(".student_checkbox")
    let checked = [];
    for (let student of students) {
        if (student.checked) {
            checked.push(student.id)
        }
    }
    return checked;
}

function count_students(is_checked) {
    let students = document.querySelectorAll("input[type=checkbox].student_checkbox")
    let count = 0
    if (!is_checked) {
        return students.length
    }
    for (let st of students) {
        if (st.checked) {
            count += 1
        }
    }
    return count
}
let main_bl = document.querySelector("div.main_block")
let checked_count = document.querySelector("div.checked_count")
let students_count = document.querySelector("div.checked_count span")

main_bl.addEventListener("change", (e) => {
    let count = count_students(true)
    console.log(`Выбрано ${count} учеников`)
    students_count.textContent = `${count}`
})

document.addEventListener("DOMContentLoaded", (e) => {
    let all_count = document.querySelector("div.checked_count span.all_count")
    all_count.textContent = `${count_students(false)}`
})

for (let btn of document.querySelectorAll(".generate_btn")) {
    btn.addEventListener("click", to_generate)
}


const select_all_btn = document.querySelector("#all_checkboxes")


