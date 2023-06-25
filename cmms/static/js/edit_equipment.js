function parseJSON(response) {
    return response.json()
}

const self = document.currentScript

document.addEventListener("DOMContentLoaded", () => {
    const modal = getModal(self.dataset.id)
    
    if (modal)
        modal.addEventListener("modalOpen", () => {
            const spinner = modal.querySelector("#spinner")

            spinner.classList.remove("hidden")
            modal.classList.add("overflow-hidden")

            const id = modal.querySelector("input[name='id']").getAttribute("value")
            fetch(`/api/v1/equipment/${id}`)
                .then(parseJSON)
                .then((data) => {
                    spinner.classList.add("hidden")
                    modal.classList.remove("overflow-hidden")

                    modal.querySelector("input[name='tag']").value = data.tag
                    modal.querySelector("input[name='name']").value = data.name
                    modal.querySelector("input[name='manufacture']").value = data.manufacture
                    modal.querySelector("select[name='pm_frequency']").value = data.pm_frequency
                    modal.querySelector("select[name='work_place']").value = data.work_place
                    modal.querySelector("input[name='cost']").value = data.cost
                    modal.querySelector("input[name='location']").value = data.location
                    modal.querySelector("input[name='installation_date']").value = data.installation_date
                    modal.querySelector("input[name='warranty_date']").value = data.warranty_date
                    modal.querySelector("input[name='arrival_date']").value = data.arrival_date
                    modal.querySelector("input[name='note']").value = data.note
                })
        })
})
