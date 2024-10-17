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
        document.getElementById('cpf-error').style.display = 'none'
        var cpf = input.value.replace(/[^\d]/g, '')
        if (cpf.length === 11){
            var Soma = 0
            var Resto
            for (i=1; i<=9; i++)
              Soma = Soma + parseInt(cpf.substring(i-1, i)) * (11 - i)
          
            Resto = (Soma * 10) % 11
          
            if ((Resto == 10) || (Resto == 11)) 
              Resto = 0
          
            if (Resto != parseInt(cpf.substring(9, 10)) )
                
                return document.getElementById('cpf-error').style.display = 'block'
            
            Soma = 0
          
            for (i = 1; i <= 10; i++)
              Soma = Soma + parseInt(cpf.substring(i-1, i)) * (12 - i)
          
            Resto = (Soma * 10) % 11
          
            if ((Resto == 10) || (Resto == 11)) 
              Resto = 0
          
            if (Resto != parseInt(cpf.substring(10, 11) ) )
                
                return document.getElementById('cpf-error').style.display = 'block'
            
                
                
            input.value = formatarCpf(input.value)
          }
       
    } else if (input.id === 'cep') {
        document.getElementById('cep-error').style.display = 'none'
        var cep = input.value.replace(/\D/g, '')
        if (cep.length === 8) {
            fetch(`https://viacep.com.br/ws/${cep}/json/`)
                .then(response => response.json())
                .then(data => {
                    if (!data.erro) {
                        document.getElementById('rua').value = data.logradouro
                        document.getElementById('bairro').value = data.bairro
                        document.getElementById('cidade').value = data.localidade
                        document.getElementById('estado').value = data.uf
                    } else {
                        
                        limparFormulario()
                        document.getElementById('rua').readOnly = true
                        document.getElementById('estado').readOnly = true
                        document.getElementById('cidade').readOnly = true
                        document.getElementById('bairro').readOnly = true
                        return document.getElementById('cep-error').style.display = 'block'
                    }
                })
                document.getElementById('rua').readOnly = false
                document.getElementById('estado').readOnly = true
                document.getElementById('cidade').readOnly = true
                document.getElementById('bairro').readOnly = true
                input.value = formatarCep(input.value)
            }
            
            limparFormulario()
    } else if (input.id === 'telefone') {
        input.value = formatarTelefone(input.value)
    }
}
function limparFormulario() {
    document.getElementById('rua').value = ''
    document.getElementById('bairro').value = ''
    document.getElementById('cidade').value = ''
    document.getElementById('estado').value = ''
}
const exampleModal = document.getElementById('exampleModal')
if (exampleModal) {
  exampleModal.addEventListener('show.bs.modal', event => {
    // Button that triggered the modal
    const button = event.relatedTarget
    // Extract info from data-bs-* attributes
    const recipient = button.getAttribute('data-bs-whatever')
    // If necessary, you could initiate an Ajax request here
    // and then do the updating in a callback.

    // Update the modal's content.
    const modalTitle = exampleModal.querySelector('.modal-title')
    const modalBodyInput = exampleModal.querySelector('.modal-body input')

    modalTitle.textContent = `New message to ${recipient}`
    modalBodyInput.value = recipient
  })
  
}

function selecionarCidades(){
    const estadoSelect = document.getElementById('naturalidade_estado');
    const selectedOptionEstado = estadoSelect.options[estadoSelect.selectedIndex] // Pega a opção selecionada
    const estadoId = selectedOptionEstado.getAttribute('data-id')
    const cidadeSelect = document.getElementById('naturalidade_cidade')
    const selectedOptionCidade = estadoSelect.options[cidadeSelect.selectedIndex] // Pega a opção selecionada
    const Cidade = selectedOptionCidade.getAttribute('data-id')
    

    // Fazer a requisição para a API do IBGE para buscar as cidades do estado selecionado
    axios.get(`https://servicodados.ibge.gov.br/api/v1/localidades/estados/${estadoId}/municipios`)
        .then(response => {
            const cidades = response.data
            
            
            // Adicionar as novas opções de cidades
            cidades.forEach(cidade => {
                const option = document.createElement('option')
                option.value = cidade.nome
                option.textContent = cidade.nome
                cidadeSelect.appendChild(option)
            })
        })
        .catch(error => {
            console.error('Erro ao buscar as cidades:', error)
            cidadeSelect.innerHTML = '<option value="" disabled selected>Erro ao carregar cidades</option>'
        })
        
    }