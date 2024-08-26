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
        document.getElementById('cpf-error').style.display = 'none';
        var cpf = input.value.replace(/[^\d]/g, '')
        if (cpf.length === 11){
            var Soma = 0
            var Resto
            for (i=1; i<=9; i++)
              Soma = Soma + parseInt(cpf.substring(i-1, i)) * (11 - i);
          
            Resto = (Soma * 10) % 11
          
            if ((Resto == 10) || (Resto == 11)) 
              Resto = 0
          
            if (Resto != parseInt(cpf.substring(9, 10)) )
                
                return document.getElementById('cpf-error').style.display = 'block';
            
            Soma = 0
          
            for (i = 1; i <= 10; i++)
              Soma = Soma + parseInt(cpf.substring(i-1, i)) * (12 - i)
          
            Resto = (Soma * 10) % 11
          
            if ((Resto == 10) || (Resto == 11)) 
              Resto = 0
          
            if (Resto != parseInt(cpf.substring(10, 11) ) )
                
                return document.getElementById('cpf-error').style.display = 'block';
            
                
                
            input.value = formatarCpf(input.value)
          }
       
    } else if (input.id === 'cep') {
        document.getElementById('cep-error').style.display = 'none';
        var cep = input.value.replace(/\D/g, '');
        if (cep.length === 8) {
            fetch(`https://viacep.com.br/ws/${cep}/json/`)
                .then(response => response.json())
                .then(data => {
                    if (!data.erro) {
                        document.getElementById('rua').value = data.logradouro;
                        document.getElementById('bairro').value = data.bairro;
                        document.getElementById('cidade').value = data.localidade;
                        document.getElementById('estado').value = data.uf;
                    } else {
                        
                        limparFormulario()
                        document.getElementById('rua').disabled  = true;
                        document.getElementById('numero').disabled  = true;
                        document.getElementById('estado').disabled  = true;
                        document.getElementById('cidade').disabled  = true;
                        document.getElementById('bairro').disabled  = true;
                        return document.getElementById('cep-error').style.display = 'block';
                    }
                })
                .catch(error => {
                    limparFormulario()
                    document.getElementById('rua').disabled  = true;
                    document.getElementById('numero').disabled  = true;
                    document.getElementById('estado').disabled  = true;
                    document.getElementById('cidade').disabled  = true;
                    document.getElementById('bairro').disabled  = true;
                    
                });
                input.value = formatarCep(input.value)
            }
            
            limparFormulario();
    } else if (input.id === 'telefone') {
        input.value = formatarTelefone(input.value)
    }
}
function limparFormulario() {
    document.getElementById('rua').value = '';
    document.getElementById('bairro').value = '';
    document.getElementById('cidade').value = '';
    document.getElementById('estado').value = '';
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