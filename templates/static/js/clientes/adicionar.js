$('#btn-novo-carro').on('click', () => {

  qtd_carros = $('input[name="qtd_carros"]').val();
  qtd_carros = parseInt(qtd_carros);
  qtd_carros += 1;

  var html_carros = ` \
    <div class="row carro" id="carro-${qtd_carros}"> \
      <div class="col-md-5 mb-3"> \
        <label for="modelo" class="form-label">Modelo</label> \
        <input type="text" name="modelo" id="modelo" class="form-control"> \
      </div> \
      <div class="col-md-3 mb-3"> \
        <label for="placa" class="form-label">Placa</label> \
        <input type="text" name="placa" id="placa" class="form-control"> \
      </div> \
      <div class="col-md-3 mb-3"> \
        <label for="ano" class="form-label">Ano</label> \
        <input type="text" name="ano" id="ano" class="form-control"> \
      </div> \
      <div class="col-md-1 mb-3"> \
        <label for="" class="form-label">Exluir</label> \
        <button type="button" class="btn btn-danger form-control" onclick="excluirCarro('carro-${qtd_carros}')"><i class="mdi mdi-delete"></i></button> \
      </div> \
    </div> \
  `;

  $('#form-carros').append(html_carros);
  $('input[name="qtd_carros"]').val(qtd_carros);
});

const excluirCarro = (cod_carro) => {
  obj = $(`#${cod_carro}`);
  obj.remove();
};

$('.btn-salvar-cliente').on('click', async () => {
  const form_cliente = $('#form-cliente').serializeArray().reduce((output, value) => {
    output[value.name] = value.value
    return output
  }, {});

  form_cliente['carros'] = [];
  const list_carros = $('#form-carros .carro');
  list_carros.map((index, carro) => {
    form_cliente.carros.push({
      'modelo': $(carro).find('input[name="modelo"]').val(),
      'placa': $(carro).find('input[name="placa"]').val(),
      'ano': $(carro).find('input[name="ano"]').val(),
    });
  });

  await fetch('http://localhost:8000/clientes/cadastrar/', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val(),
    },
    body: JSON.stringify(form_cliente),
  }).then((result) => {
    result.json().then((data) => {
      if (data.result == 'success') {
        sessionStorage.setItem('PAGE_NOTIFICATION', JSON.stringify(data));
        window.location.replace('http://localhost:8000/clientes/');
      }

      $.NotificationApp.send('Notificação: ', data.message, 'top-right', '#bf441d', data.result, 3e3, 1, 'slide');
    });
  })

});