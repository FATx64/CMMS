function parseJSON(response) {
  return response.json()
}

document.addEventListener("DOMContentLoaded", () => {
    const modal = getModal("edit_workplace")
    modal.addEventListener("modalOpen", () => {
        const spinner = modal.querySelector("#spinner")

        spinner.classList.remove("hidden")
        modal.classList.add("overflow-hidden")

        const id = modal.querySelector("input[name='id']").getAttribute("value")
        fetch(`/dashboard/workplace/${id}`)
            .then(parseJSON)
            .then((data) => {
                spinner.classList.add("hidden")
                modal.classList.remove("overflow-hidden")

                modal.querySelector("input[name='name']").value = data.name
                modal.querySelector("input[name='code']").value = data.code
                modal.querySelector("input[name='location']").value = data.location
            })
    })
})
