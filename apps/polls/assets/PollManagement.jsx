var api = require('adhocracy4').api
var React = require('react')
var django = require('django')
var update = require('react-addons-update')
var FlipMove = require('react-flip-move')
var QuestionForm = require('./QuestionForm')

let PollManagement = React.createClass({
  getInitialState: function () {
    return {
      questions: this.props.poll.questions,
      errors: [],
      successMessage: ''
    }
  },

  maxLocalKey: 0,
  getNextLocalKey: function () {
    /** Get an artificial key for non-committed items.
     *
     *  The key is prefixed to prevent collisions with real database keys.
     */
    this.maxLocalKey++
    return 'local_' + this.maxLocalKey
  },

  /*
  |--------------------------------------------------------------------------
  | Question state related handlers
  |--------------------------------------------------------------------------
  */

  getNewQuestion: function (label) {
    return {
      label: label,
      key: this.getNextLocalKey(),
      choices: []
    }
  },

  handleUpdateQuestionLabel: function (index, label) {
    var diff = {}
    diff[index] = {$merge: {label: label}}

    this.setState({
      questions: update(this.state.questions, diff)
    })
  },

  handleMoveQuestionUp: function (index) {
    var question = this.state.questions[index]
    var diff = {$splice: [[index, 1], [index - 1, 0, question]]}

    this.setState({
      questions: update(this.state.questions, diff)
    })
  },

  handleMoveQuestionDown: function (index) {
    var question = this.state.questions[index]
    var diff = {$splice: [[index, 1], [index + 1, 0, question]]}

    this.setState({
      questions: update(this.state.questions, diff)
    })
  },

  handleAppendQuestion: function () {
    var newQuestion = this.getNewQuestion('')
    var diff = {$push: [newQuestion]}

    this.setState({
      questions: update(this.state.questions, diff)
    })
  },

  handleDeleteQuestion: function (index) {
    var diff = {$splice: [[index, 1]]}

    this.setState({
      questions: update(this.state.questions, diff)
    })
  },

  /*
  |--------------------------------------------------------------------------
  | Choice state related handlers
  |--------------------------------------------------------------------------
  */

  getNewChoice: function (label) {
    return {
      label: label,
      key: this.getNextLocalKey()
    }
  },

  handleUpdateChoiceLabel: function (questionIndex, choiceIndex, label) {
    var diff = {}
    diff[questionIndex] = {choices: {}}
    diff[questionIndex]['choices'][choiceIndex] = {$merge: {label: label}}

    this.setState({
      questions: update(this.state.questions, diff)
    })
  },

  handleAppendChoice: function (questionIndex) {
    var newChoice = this.getNewChoice('')
    var diff = {}
    diff[questionIndex] = {choices: {$push: [newChoice]}}

    this.setState({
      questions: update(this.state.questions, diff)
    })
  },

  handleDeleteChoice: function (questionIndex, choiceIndex) {
    var diff = {}
    diff[questionIndex] = {choices: {$splice: [[choiceIndex, 1]]}}

    this.setState({
      questions: update(this.state.questions, diff)
    })
  },

  /*
  |--------------------------------------------------------------------------
  | Poll form and submit logic
  |--------------------------------------------------------------------------
  */

  handleSubmit: function (e) {
    e.preventDefault()

    let data = {
      questions: this.state.questions
    }

    api.poll.change(data, this.props.poll.id)
      .done(function (data) {
        this.setState({
          successMessage: django.gettext('The poll has been updated.')
        })

        setTimeout(function () {
          // TODO: reset errors
          this.setState({
            successMessage: ''
          })
        }.bind(this), 1500)
      }.bind(this))
      .fail(function (xhr, status, err) {
        // TODO: re-set state only if errors occured
        this.setState({
          errors: xhr.responseJSON.questions || []
        })
      }.bind(this))
  },

  render: function () {
    return (
      <form onSubmit={this.handleSubmit}>
        { this.state.successMessage
          ? <p className="alert alert-success ">
            {this.state.successMessage}
          </p> : null
        }

        <FlipMove easing="cubic-bezier(0.25, 0.5, 0.75, 1)">
          {
            this.state.questions.map(function (question, index) {
              var key = question.id || question.key
              var errors = this.state.errors && this.state.errors[index] ? this.state.errors[index] : {}
              return (
                <QuestionForm
                  key={key}
                  index={index}
                  question={question}
                  updateQuestionLabel={this.handleUpdateQuestionLabel}
                  moveQuestionUp={index !== 0 ? this.handleMoveQuestionUp : null}
                  moveQuestionDown={index < this.state.questions.length - 1 ? this.handleMoveQuestionDown : null}
                  deleteQuestion={this.handleDeleteQuestion}
                  errors={errors}
                  updateChoiceLabel={this.handleUpdateChoiceLabel}
                  deleteChoice={this.handleDeleteChoice}
                  appendChoice={this.handleAppendChoice}
                />
              )
            }.bind(this))
          }
        </FlipMove>

        <button
          className="button button--full"
          onClick={this.handleAppendQuestion}
          type="button">
          <i className="fa fa-plus" /> {django.gettext('add a new question')}
        </button>

        { this.state.successMessage
          ? <p className="alert alert-success ">
            {this.state.successMessage}
          </p> : null
        }

        <button type="submit" className="button button--primary">{django.gettext('save')}</button>
      </form>
    )
  }
})

module.exports = PollManagement
