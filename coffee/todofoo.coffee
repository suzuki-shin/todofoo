#
# functions
#
post_task =->
  task = $('#task').attr('value')
  $('#task').attr('value', '')
  _post '/task',
        {task: task},
        (d, s, x)->
          notify('Add ' + task)
          reflesh_tasklist()

reflesh_tasklist =->
  _reflesh_tasklist = (data, status, xhr) ->
    _l '_reflesh_tasklist'
    tasks_str = ('<tr><td><label class="checkbox"><input type="checkbox" /></label>' + t.name + '</td></tr>' for t in data).join('')
    $('#tasklist tbody').empty().append(tasks_str)
  _get '/tasklist', _reflesh_tasklist, (data, status, xhr) -> _failure_func status



#
# events
#
$ ->
  reflesh_tasklist()

  $('#task').focus()

  $('#taskpost').submit ->
    post_task()
    false

  $('.navbar').click ->
    $('.pane').toggle()
    $('.nav-icon').toggle()
