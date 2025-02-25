import { useState, useEffect } from 'react'
import './App.css'
import SearchHeader from './components/SearchHeader'
import QueryResult from './components/QueryResult'
import HistoryPanel from './components/HistoryPanel'
import ConfigPanel from './components/ConfigPanel'

function App() {
  const [queryResult, setQueryResult] = useState(null)
  const [queryHistory, setQueryHistory] = useState([])
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const [isConfigOpen, setIsConfigOpen] = useState(false)

  const languages = [
    { code: 'en', name: '英语' },
    { code: 'zh-yue', name: '粤语' },
    { code: 'zh', name: '普通话' },
    { code: 'zh-sc', name: '四川话' }
  ]

  useEffect(() => {
    fetchQueryHistory()
    const interval = setInterval(fetchQueryHistory, 30000) // 每30秒刷新一次
    return () => clearInterval(interval)
  }, [])

  const getBackendUrl = () => {
    const savedUrl = localStorage.getItem('backendUrl')
    return savedUrl || 'http://localhost:8000'
  }

  const fetchQueryHistory = async () => {
    try {
      const backendUrl = getBackendUrl()
      const response = await fetch(`${backendUrl}/api/queries`)
      const data = await response.json()
      setQueryHistory(data.queries)
    } catch (error) {
      console.error('获取历史记录失败:', error)
    }
  }

  const handleSearch = async (word, selectedLanguages, exampleCount) => {
    try {
      const backendUrl = getBackendUrl()
      const response = await fetch(`${backendUrl}/api/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          word,
          languages: selectedLanguages,
          example_count: exampleCount
        })
      })
      const data = await response.json()
      setQueryResult(data)
      fetchQueryHistory()
    } catch (error) {
      console.error('查询失败:', error)
    }
  }

  const handleDelete = async (timestamp) => {
    try {
      const backendUrl = getBackendUrl()
      const response = await fetch(`${backendUrl}/api/queries/${timestamp}`, {
        method: 'DELETE'
      })
      if (response.ok) {
        // 删除成功后更新历史记录列表
        fetchQueryHistory()
        // 如果当前显示的是被删除的记录，则清空显示
        if (queryResult && queryResult.timestamp === timestamp) {
          setQueryResult(null)
        }
      } else {
        console.error('删除失败:', await response.text())
      }
    } catch (error) {
      console.error('删除失败:', error)
    }
  }

  return (
    <div className="container">
      <SearchHeader onSearch={handleSearch} />
      <QueryResult queryResult={queryResult} languages={languages} />
      <HistoryPanel
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        queryHistory={queryHistory}
        languages={languages}
        onRecordClick={(record) => {
          setQueryResult(record);
          // setIsSidebarOpen(false);
        }}
        onDelete={handleDelete}
      />
      <div className="header-buttons">
        <button
          className="toggle-history"
          onClick={() => setIsSidebarOpen(!isSidebarOpen)}
        >
          {isSidebarOpen ? '隐藏历史' : '显示历史'}
        </button>
        <button
          className="config-button"
          onClick={() => setIsConfigOpen(true)}
        >
          ⚙️
        </button>
      </div>
      <ConfigPanel isOpen={isConfigOpen} onClose={() => setIsConfigOpen(false)} />
    </div>
  )
}

export default App
