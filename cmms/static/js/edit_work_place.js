function parseJSON(response) {
  return response.json()
}

document.addEventListener("DOMContentLoaded", () => {
    const modal = getModal("edit_form")
    modal.addEventListener("modalOpen", () => {
        const id = modal.querySelector("input[name='id']").getAttribute("value")
        fetch(`/dashboard/workplace/${id}`)
            .then(parseJSON)
            .then((data) => {
                modal.querySelector("input[name='name']").setAttribute("value", data.name)
                modal.querySelector("input[name='code']").setAttribute("value", data.code)
                modal.querySelector("input[name='location']").setAttribute("value", data.location)
            })
    })
})
