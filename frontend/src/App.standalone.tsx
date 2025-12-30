import { useState, useEffect, useRef } from 'react'
import './App.css'

interface Message {
  id: number
  type: 'user' | 'system' | 'command' | 'result' | 'ros_message'
  content: string
  timestamp: string
}

interface ROS2Node {
  name: string
  running: boolean
  messageCount: number
}

// ブラウザ内ROS2シミュレーター
class ROS2Simulator {
  private publisherInterval: NodeJS.Timeout | null = null
  private subscriberCallback: ((msg: string) => void) | null = null
  private publisherRunning = false
  private subscriberRunning = false
  private messageCounter = 0

  startPublisher(onMessage: (msg: string) => void) {
    if (this.publisherRunning) return 'パブリッシャーは既に実行中です'

    this.publisherRunning = true
    this.messageCounter = 0

    this.publisherInterval = setInterval(() => {
      const data = {
        counter: this.messageCounter,
        message: `Hello from Publisher #${this.messageCounter}`,
        timestamp: new Date().toISOString()
      }

      const jsonMsg = JSON.stringify(data, null, 2)
      onMessage(`[Publisher] 送信: ${data.message}`)

      // サブスクライバーにメッセージを配信
      if (this.subscriberRunning && this.subscriberCallback) {
        setTimeout(() => {
          this.subscriberCallback?.(jsonMsg)
        }, 100)
      }

      this.messageCounter++
    }, 2000)

    return 'パブリッシャーノードを起動しました (PID: simulated)'
  }

  stopPublisher() {
    if (!this.publisherRunning) return 'パブリッシャーは起動していません'

    if (this.publisherInterval) {
      clearInterval(this.publisherInterval)
      this.publisherInterval = null
    }

    this.publisherRunning = false
    return 'パブリッシャーノードを停止しました'
  }

  startSubscriber(onMessage: (msg: string) => void) {
    if (this.subscriberRunning) return 'サブスクライバーは既に実行中です'

    this.subscriberRunning = true
    this.subscriberCallback = (msg: string) => {
      try {
        const data = JSON.parse(msg)
        onMessage(`[Subscriber] 受信: ${data.message} (counter: ${data.counter})`)
      } catch (e) {
        onMessage(`[Subscriber] 受信: ${msg}`)
      }
    }

    return 'サブスクライバーノードを起動しました (PID: simulated)'
  }

  stopSubscriber() {
    if (!this.subscriberRunning) return 'サブスクライバーは起動していません'

    this.subscriberRunning = false
    this.subscriberCallback = null
    return 'サブスクライバーノードを停止しました'
  }

  checkStatus() {
    const nodes = []
    if (this.publisherRunning) nodes.push('/publisher_node')
    if (this.subscriberRunning) nodes.push('/subscriber_node')

    if (nodes.length === 0) {
      return '実行中のノード: なし'
    }

    return `実行中のノード:\n${nodes.map(n => `- ${n}`).join('\n')}`
  }

  listTopics() {
    return `トピック一覧:\n- /chat_topic\n- /parameter_events\n- /rosout`
  }

  getNodeStatus() {
    return {
      publisher_node: { running: this.publisherRunning, pid: null },
      subscriber_node: { running: this.subscriberRunning, pid: null }
    }
  }

  cleanup() {
    if (this.publisherInterval) {
      clearInterval(this.publisherInterval)
    }
  }
}

function App() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [nodeStatus, setNodeStatus] = useState<{
    publisher_node: { running: boolean; pid: number | null }
    subscriber_node: { running: boolean; pid: number | null }
  }>({
    publisher_node: { running: false, pid: null },
    subscriber_node: { running: false, pid: null }
  })

  const messagesEndRef = useRef<HTMLDivElement>(null)
  const simulatorRef = useRef<ROS2Simulator>(new ROS2Simulator())

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    // 初期メッセージ
    addMessage('system', 'ROS2シミュレーター（GitHub Pages版）を起動しました')
    addMessage('system', 'このバージョンはブラウザ内でROS2をシミュレートします')

    // 定期的にステータス更新
    const interval = setInterval(() => {
      setNodeStatus(simulatorRef.current.getNodeStatus())
    }, 1000)

    return () => {
      clearInterval(interval)
      simulatorRef.current.cleanup()
    }
  }, [])

  const addMessage = (type: Message['type'], content: string) => {
    setMessages((prev) => [
      ...prev,
      {
        id: Date.now() + Math.random(),
        type,
        content,
        timestamp: new Date().toLocaleTimeString('ja-JP')
      }
    ])
  }

  const interpretCommand = (userInput: string): string => {
    const msg = userInput.toLowerCase()

    if (msg.includes('パブリッシャ') && (msg.includes('起動') || msg.includes('開始') || msg.includes('スタート'))) {
      return 'start_publisher'
    } else if (msg.includes('サブスクライバ') && (msg.includes('起動') || msg.includes('開始') || msg.includes('スタート'))) {
      return 'start_subscriber'
    } else if (msg.includes('パブリッシャ') && (msg.includes('停止') || msg.includes('終了'))) {
      return 'stop_publisher'
    } else if (msg.includes('サブスクライバ') && (msg.includes('停止') || msg.includes('終了'))) {
      return 'stop_subscriber'
    } else if (msg.includes('状態') || msg.includes('ステータス') || msg.includes('確認')) {
      return 'check_status'
    } else if (msg.includes('トピック')) {
      return 'list_topics'
    } else {
      return 'check_status'
    }
  }

  const executeCommand = (command: string) => {
    const simulator = simulatorRef.current
    let result = ''

    switch (command) {
      case 'start_publisher':
        result = simulator.startPublisher((msg) => addMessage('ros_message', msg))
        break
      case 'start_subscriber':
        result = simulator.startSubscriber((msg) => addMessage('ros_message', msg))
        break
      case 'stop_publisher':
        result = simulator.stopPublisher()
        break
      case 'stop_subscriber':
        result = simulator.stopSubscriber()
        break
      case 'check_status':
        result = simulator.checkStatus()
        break
      case 'list_topics':
        result = simulator.listTopics()
        break
      default:
        result = `未知のコマンド: ${command}`
    }

    return result
  }

  const sendMessage = () => {
    if (!input.trim()) return

    // ユーザーメッセージを追加
    addMessage('user', input)

    // コマンド解釈
    const command = interpretCommand(input)
    addMessage('command', `実行コマンド: ${command}`)

    // コマンド実行
    const result = executeCommand(command)
    addMessage('result', result)

    setInput('')
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>ROS2 AI Web Agent (GitHub Pages版)</h1>
        <div className="status-bar">
          <span className="status-indicator connected">
            ブラウザ内シミュレーション
          </span>
          <div className="node-status">
            <span className={nodeStatus.publisher_node.running ? 'node-running' : 'node-stopped'}>
              Publisher: {nodeStatus.publisher_node.running ? '実行中' : '停止'}
            </span>
            <span className={nodeStatus.subscriber_node.running ? 'node-running' : 'node-stopped'}>
              Subscriber: {nodeStatus.subscriber_node.running ? '実行中' : '停止'}
            </span>
          </div>
        </div>
      </header>

      <main className="main">
        <div className="messages-container">
          {messages.length <= 2 && (
            <div className="welcome-message">
              <h2>ようこそ!</h2>
              <p>このバージョンはGitHub Pages用で、ブラウザ内でROS2をシミュレートします</p>
              <div className="examples">
                <h3>試してみよう:</h3>
                <ul>
                  <li>"パブリッシャーを起動して"</li>
                  <li>"サブスクライバーを開始"</li>
                  <li>"通信状態を確認"</li>
                  <li>"トピック一覧を表示"</li>
                </ul>
              </div>
            </div>
          )}

          {messages.map((msg) => (
            <div key={msg.id} className={`message message-${msg.type}`}>
              <div className="message-header">
                <span className="message-type">
                  {msg.type === 'user' ? 'あなた' :
                   msg.type === 'system' ? 'システム' :
                   msg.type === 'command' ? 'コマンド' :
                   msg.type === 'ros_message' ? 'ROS2' : '結果'}
                </span>
                <span className="message-time">{msg.timestamp}</span>
              </div>
              <div className="message-content">{msg.content}</div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        <div className="input-container">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="メッセージを入力... (Enter で送信)"
            rows={3}
          />
          <button
            onClick={sendMessage}
            disabled={!input.trim()}
            className="send-button"
          >
            送信
          </button>
        </div>
      </main>
    </div>
  )
}

export default App
