import { useState, useEffect, useRef } from 'react'
import './App.css'

interface Message {
  id: number
  type: 'user' | 'system' | 'command' | 'result'
  content: string
  timestamp: string
}

interface NodeStatus {
  publisher_node: { running: boolean; pid: number | null }
  subscriber_node: { running: boolean; pid: number | null }
}

function App() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [ws, setWs] = useState<WebSocket | null>(null)
  const [connected, setConnected] = useState(false)
  const [nodeStatus, setNodeStatus] = useState<NodeStatus | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    connectWebSocket()
    fetchNodeStatus()

    const interval = setInterval(fetchNodeStatus, 3000)
    return () => {
      clearInterval(interval)
      ws?.close()
    }
  }, [])

  const connectWebSocket = () => {
    const wsUrl = `ws://${window.location.hostname}:8000/ws`
    const websocket = new WebSocket(wsUrl)

    websocket.onopen = () => {
      console.log('WebSocket connected')
      setConnected(true)
    }

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      console.log('Received:', data)

      if (data.type === 'connection') {
        addMessage('system', data.message)
      } else if (data.type === 'command_interpreted') {
        addMessage('command', `実行コマンド: ${data.command}`)
      } else if (data.type === 'command_result') {
        addMessage('result', data.output)
      }
    }

    websocket.onclose = () => {
      console.log('WebSocket disconnected')
      setConnected(false)
      setTimeout(connectWebSocket, 3000)
    }

    websocket.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    setWs(websocket)
  }

  const fetchNodeStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/nodes/status')
      const data = await response.json()
      setNodeStatus(data)
    } catch (error) {
      console.error('Failed to fetch node status:', error)
    }
  }

  const addMessage = (type: Message['type'], content: string) => {
    setMessages((prev) => [
      ...prev,
      {
        id: Date.now(),
        type,
        content,
        timestamp: new Date().toLocaleTimeString('ja-JP')
      }
    ])
  }

  const sendMessage = () => {
    if (!input.trim() || !ws || !connected) return

    addMessage('user', input)

    ws.send(JSON.stringify({ message: input }))
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
        <h1>ROS2 AI Web Agent</h1>
        <div className="status-bar">
          <span className={`status-indicator ${connected ? 'connected' : 'disconnected'}`}>
            {connected ? '接続中' : '切断'}
          </span>
          {nodeStatus && (
            <div className="node-status">
              <span className={nodeStatus.publisher_node.running ? 'node-running' : 'node-stopped'}>
                Publisher: {nodeStatus.publisher_node.running ? '実行中' : '停止'}
              </span>
              <span className={nodeStatus.subscriber_node.running ? 'node-running' : 'node-stopped'}>
                Subscriber: {nodeStatus.subscriber_node.running ? '実行中' : '停止'}
              </span>
            </div>
          )}
        </div>
      </header>

      <main className="main">
        <div className="messages-container">
          {messages.length === 0 && (
            <div className="welcome-message">
              <h2>ようこそ!</h2>
              <p>AIエージェントに自然言語で指示を出してください</p>
              <div className="examples">
                <h3>例:</h3>
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
                   msg.type === 'command' ? 'コマンド' : '結果'}
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
            disabled={!connected}
          />
          <button
            onClick={sendMessage}
            disabled={!connected || !input.trim()}
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
