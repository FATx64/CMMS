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
                        query GetAgent($id: Int!) {
                            agent(id: $id) {
                                id
                                agentId
                                fullName
                                address
                                phoneNumber
                                email
                                note
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
                    const agent = result.data.agent
                    spinner.classList.add("hidden")
                    modal.classList.remove("overflow-hidden")

                    modal.querySelector("input[name='agent_id']").value = agent.agentId
                    modal.querySelector("input[name='full_name']").value = agent.fullName
                    modal.querySelector("input[name='address']").value = agent.address
                    modal.querySelector("input[name='phone_number']").value = agent.phoneNumber
                    modal.querySelector("input[name='email']").value = agent.email
                    modal.querySelector("input[name='note']").value = agent.note
                })
        })
})
