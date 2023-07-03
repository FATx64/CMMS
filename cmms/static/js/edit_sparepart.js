const self = document.currentScript

document.addEventListener("DOMContentLoaded", () => {
    const modal = getModal(self.dataset.id)
    
    if (modal)
        modal.addEventListener("modalOpen", () => {
            const spinner = modal.querySelector("#spinner")

            spinner.classList.remove("hidden")
            modal.classList.add("overflow-hidden")

            const id = modal.querySelector("input[name='id']").getAttribute("value")
            fetch("/graphql", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    query: `
                        query GetSparepart($id: Int!) {
                            sparepart(id: $id) {
                                id
                                tag
                                name
                                equipment {
                                    id
                                }
                                amount
                            }
                        }
                    `,
                    variables: {
                        id: Number.parseInt(id)
                    }
                })
            })
                .then(parseJSON)
                .then((result) => {
                    const sparepart = result.data.sparepart
                    spinner.classList.add("hidden")
                    modal.classList.remove("overflow-hidden")

                    modal.querySelector("input[name='tag']").value = sparepart.tag
                    modal.querySelector("input[name='name']").value = sparepart.name
                    modal.querySelector("select[name='equipment']").value = sparepart.equipment.id
                    modal.querySelector("input[name='amount']").value = sparepart.amount
                })
        })
})
