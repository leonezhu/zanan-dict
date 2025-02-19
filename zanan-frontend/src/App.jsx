import { useState, useEffect } from 'react'
import './App.css'
import SearchHeader from './components/SearchHeader'
import QueryResult from './components/QueryResult'
import HistoryPanel from './components/HistoryPanel'

function App() {
  const [queryResult, setQueryResult] = useState(null)
  const [queryHistory, setQueryHistory] = useState([])
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)

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

  const fetchQueryHistory = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/queries')
      const data = await response.json()
      setQueryHistory(data.queries)
    } catch (error) {
      console.error('获取历史记录失败:', error)
    }
  }

  const handleSearch = async (word, selectedLanguages) => {
    try {
      const response = await fetch('http://localhost:8000/api/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          word,
          languages: selectedLanguages
        })
      })
      const data = await response.json()
      setQueryResult(data)
      fetchQueryHistory()
      setIsSidebarOpen(true) // 查询成功后显示侧边栏
    } catch (error) {
      console.error('查询失败:', error)
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
        onRecordClick={(record) => setQueryResult(record)}
      />
      <button
        className="toggle-history"
        onClick={() => setIsSidebarOpen(!isSidebarOpen)}
      >
        {isSidebarOpen ? '隐藏历史' : '显示历史'}
      </button>
    </div>
  )
}

export default App
