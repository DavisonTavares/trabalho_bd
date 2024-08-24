// Função para formatar o CPF
function formatarCpf(cpf) {
    cpf = cpf.replace(/\D/g, '') // Remove caracteres não numéricos
    cpf = cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4') // Adiciona pontos e hífen
    return cpf
}
// Função para formatar o CEP
function formatarCep(cep) {
    cep = cep.replace(/\D/g, '') // Remove caracteres não numéricos
    cep = cep.replace(/(\d{5})(\d{3})/, '$1-$2') // Adiciona hífen
    return cep
}
function formatarTelefone(telefone) {
    telefone = telefone.replace(/\D/g, '') // Remove caracteres não numéricos
    telefone = telefone.replace(/^(\d{2})(\d{5})(\d{4})$/, '($1) $2-$3') // Adiciona parênteses, espaço e hífen
    return telefone
}
// Função chamada quando o usuário digita nos campos
function applyMask(event) {
    const input = event.target
    if (input.id === 'cpf') {
        input.value = formatarCpf(input.value)
    } else if (input.id === 'cep') {
        input.value = formatarCep(input.value)
    } else if (input.id === 'telefone') {
        input.value = formatarTelefone(input.value)
    }
}

