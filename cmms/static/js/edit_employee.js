const self = document.currentScript

document.addEventListener("DOMContentLoaded", () => {
    const modal = getModal(self.dataset.id)
    
    if (modal)
        modal.addEventListener("modalOpen", () => {
            const spinner = modal.querySelector("#spinner")

            spinner.classList.remove("hidden")
            modal.classList.add("overflow-hidden")

            const id = modal.querySelector("input[name='id']").getAttribute("value")
            fetch(`/api/v1/users/${id}`)
                .then(parseJSON)
                .then((data) => {
                    spinner.classList.add("hidden")
                    modal.classList.remove("overflow-hidden")

                    modal.querySelector("input[name='employee_id']").value = data.employee_id
                    modal.querySelector("input[name='first_name']").value = data.first_name
                    modal.querySelector("input[name='last_name']").value = data.last_name
                    modal.querySelector("input[name='phone_number']").value = data.phone_number
                    modal.querySelector("input[name='date_of_birth']").value = data.date_of_birth
                    modal.querySelector("input[name='address']").value = data.address
                    modal.querySelector("input[name='work_hour']").value = data.work_hour
                    modal.querySelector("select[name='work_place']").value = data.work_place
                })
        })
})
