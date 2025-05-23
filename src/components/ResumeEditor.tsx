import React, { useState, useRef } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import { PDFDocument } from 'pdf-lib';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, Download, FileText, Trash2, Edit3, Plus, X, Check, ChevronLeft, ChevronRight } from 'lucide-react';
import TextareaAutosize from 'react-textarea-autosize';

pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.js`;

interface ResumeEditorProps {
  isDark: boolean;
  onClose: () => void;
}

interface Annotation {
  id: string;
  pageNumber: number;
  x: number;
  y: number;
  text: string;
  type: 'comment' | 'suggestion' | 'highlight';
}

export function ResumeEditor({ isDark, onClose }: ResumeEditorProps) {
  const [file, setFile] = useState<File | null>(null);
  const [numPages, setNumPages] = useState<number>(0);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [scale, setScale] = useState<number>(1.5);
  const [annotations, setAnnotations] = useState<Annotation[]>([]);
  const [selectedAnnotation, setSelectedAnnotation] = useState<Annotation | null>(null);
  const [isAddingAnnotation, setIsAddingAnnotation] = useState(false);
  const [newAnnotation, setNewAnnotation] = useState<Partial<Annotation> | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === 'application/pdf') {
      setFile(file);
      setCurrentPage(1);
      setAnnotations([]);
    }
  };

  const handleDocumentLoadSuccess = ({ numPages }: { numPages: number }) => {
    setNumPages(numPages);
  };

  const handlePageClick = (event: React.MouseEvent<HTMLDivElement>) => {
    if (!isAddingAnnotation) return;

    const container = containerRef.current;
    if (!container) return;

    const rect = container.getBoundingClientRect();
    const x = ((event.clientX - rect.left) / scale);
    const y = ((event.clientY - rect.top) / scale);

    setNewAnnotation({
      pageNumber: currentPage,
      x,
      y,
      type: 'comment'
    });
  };

  const handleAnnotationSave = () => {
    if (newAnnotation?.text?.trim()) {
      setAnnotations(prev => [...prev, {
        ...newAnnotation as Annotation,
        id: Math.random().toString(36).substr(2, 9)
      }]);
    }
    setNewAnnotation(null);
    setIsAddingAnnotation(false);
  };

  const handleAnnotationDelete = (id: string) => {
    setAnnotations(prev => prev.filter(a => a.id !== id));
    setSelectedAnnotation(null);
  };

  const downloadWithAnnotations = async () => {
    if (!file) return;

    try {
      const existingPdfBytes = await file.arrayBuffer();
      const pdfDoc = await PDFDocument.load(existingPdfBytes);
      
      // Here we would add annotations to the PDF
      // This is a simplified version - in production you'd want to properly
      // convert the annotations to PDF annotations

      const pdfBytes = await pdfDoc.save();
      const blob = new Blob([pdfBytes], { type: 'application/pdf' });
      const url = URL.createObjectURL(blob);
      
      const a = document.createElement('a');
      a.href = url;
      a.download = 'annotated-resume.pdf';
      a.click();
      
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error saving PDF:', error);
    }
  };

  return (
    <div className="fixed inset-0 bg-gray-100 flex flex-col">
      {/* Header */}
      <div className={`
        flex items-center justify-between px-6 py-4 border-b
        ${isDark ? 'bg-gray-900 border-gray-700' : 'bg-white border-gray-200'}
      `}>
        <div className="flex items-center gap-4">
          <button
            onClick={onClose}
            className={`
              p-2 rounded-lg transition-colors
              ${isDark 
                ? 'hover:bg-gray-800 text-gray-400 hover:text-gray-300' 
                : 'hover:bg-gray-100 text-gray-600 hover:text-gray-900'
              }
            `}
          >
            <ChevronLeft size={20} />
          </button>
          <h1 className={`text-xl font-semibold ${isDark ? 'text-white' : 'text-gray-900'}`}>
            Resume Editor
          </h1>
        </div>

        <div className="flex items-center gap-3">
          {file && (
            <>
              <button
                onClick={() => setIsAddingAnnotation(!isAddingAnnotation)}
                className={`
                  px-4 py-2 rounded-lg flex items-center gap-2 transition-colors
                  ${isAddingAnnotation
                    ? isDark
                      ? 'bg-blue-500 text-white'
                      : 'bg-blue-600 text-white'
                    : isDark
                      ? 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }
                `}
              >
                <Plus size={16} />
                Add Comment
              </button>
              <button
                onClick={downloadWithAnnotations}
                className={`
                  px-4 py-2 rounded-lg flex items-center gap-2
                  ${isDark
                    ? 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }
                `}
              >
                <Download size={16} />
                Download
              </button>
            </>
          )}
          <label className={`
            px-4 py-2 rounded-lg flex items-center gap-2 cursor-pointer
            ${isDark
              ? 'bg-blue-500 text-white hover:bg-blue-600'
              : 'bg-blue-600 text-white hover:bg-blue-700'
            }
          `}>
            <Upload size={16} />
            Upload PDF
            <input
              type="file"
              accept=".pdf"
              onChange={handleFileChange}
              className="hidden"
            />
          </label>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-hidden flex">
        {/* PDF Viewer */}
        <div 
          ref={containerRef}
          className="flex-1 overflow-auto p-8"
          onClick={handlePageClick}
        >
          {file ? (
            <div className="max-w-4xl mx-auto">
              <Document
                file={file}
                onLoadSuccess={handleDocumentLoadSuccess}
                className="pdf-document"
              >
                <Page
                  pageNumber={currentPage}
                  scale={scale}
                  className={`
                    relative rounded-lg shadow-lg
                    ${isDark ? 'bg-gray-800' : 'bg-white'}
                  `}
                  renderAnnotationLayer={false}
                  renderTextLayer={false}
                />

                {/* Annotations */}
                {annotations
                  .filter(a => a.pageNumber === currentPage)
                  .map(annotation => (
                    <div
                      key={annotation.id}
                      style={{
                        position: 'absolute',
                        left: `${annotation.x * scale}px`,
                        top: `${annotation.y * scale}px`,
                      }}
                      className="cursor-pointer"
                      onClick={(e) => {
                        e.stopPropagation();
                        setSelectedAnnotation(annotation);
                      }}
                    >
                      <div className={`
                        w-6 h-6 rounded-full flex items-center justify-center
                        ${isDark ? 'bg-blue-500 text-white' : 'bg-blue-600 text-white'}
                      `}>
                        <Edit3 size={12} />
                      </div>
                    </div>
                  ))}

                {/* New Annotation */}
                {newAnnotation && (
                  <motion.div
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    style={{
                      position: 'absolute',
                      left: `${newAnnotation.x * scale}px`,
                      top: `${newAnnotation.y * scale}px`,
                    }}
                    className={`
                      w-80 rounded-lg shadow-lg p-4
                      ${isDark ? 'bg-gray-800' : 'bg-white'}
                    `}
                    onClick={e => e.stopPropagation()}
                  >
                    <TextareaAutosize
                      autoFocus
                      placeholder="Add your comment..."
                      className={`
                        w-full resize-none rounded-lg p-2 mb-3
                        ${isDark
                          ? 'bg-gray-700 text-white placeholder:text-gray-400 border-gray-600'
                          : 'bg-gray-50 text-gray-900 placeholder:text-gray-500 border-gray-200'
                        }
                        border focus:outline-none focus:ring-2 focus:ring-blue-500
                      `}
                      value={newAnnotation.text || ''}
                      onChange={e => setNewAnnotation(prev => ({ ...prev!, text: e.target.value }))}
                    />
                    <div className="flex justify-end gap-2">
                      <button
                        onClick={() => {
                          setNewAnnotation(null);
                          setIsAddingAnnotation(false);
                        }}
                        className={`
                          p-2 rounded-lg
                          ${isDark
                            ? 'hover:bg-gray-700 text-gray-400'
                            : 'hover:bg-gray-100 text-gray-600'
                          }
                        `}
                      >
                        <X size={16} />
                      </button>
                      <button
                        onClick={handleAnnotationSave}
                        className={`
                          p-2 rounded-lg
                          ${isDark
                            ? 'hover:bg-gray-700 text-green-400'
                            : 'hover:bg-gray-100 text-green-600'
                          }
                        `}
                      >
                        <Check size={16} />
                      </button>
                    </div>
                  </motion.div>
                )}
              </Document>

              {/* Page Navigation */}
              {numPages > 1 && (
                <div className={`
                  fixed bottom-6 left-1/2 -translate-x-1/2
                  flex items-center gap-4 px-4 py-2 rounded-lg shadow-lg
                  ${isDark ? 'bg-gray-800' : 'bg-white'}
                `}>
                  <button
                    onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                    disabled={currentPage === 1}
                    className={`
                      p-1 rounded-lg transition-colors
                      ${currentPage === 1
                        ? isDark
                          ? 'text-gray-600'
                          : 'text-gray-400'
                        : isDark
                          ? 'text-gray-400 hover:text-gray-300 hover:bg-gray-700'
                          : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                      }
                    `}
                  >
                    <ChevronLeft size={20} />
                  </button>
                  <span className={isDark ? 'text-gray-300' : 'text-gray-700'}>
                    Page {currentPage} of {numPages}
                  </span>
                  <button
                    onClick={() => setCurrentPage(p => Math.min(numPages, p + 1))}
                    disabled={currentPage === numPages}
                    className={`
                      p-1 rounded-lg transition-colors
                      ${currentPage === numPages
                        ? isDark
                          ? 'text-gray-600'
                          : 'text-gray-400'
                        : isDark
                          ? 'text-gray-400 hover:text-gray-300 hover:bg-gray-700'
                          : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                      }
                    `}
                  >
                    <ChevronRight size={20} />
                  </button>
                </div>
              )}
            </div>
          ) : (
            <div className={`
              max-w-md mx-auto mt-20 p-8 rounded-xl border-2 border-dashed text-center
              ${isDark
                ? 'border-gray-700 bg-gray-800'
                : 'border-gray-300 bg-white'
              }
            `}>
              <FileText 
                size={48} 
                className={`mx-auto mb-4 ${isDark ? 'text-gray-600' : 'text-gray-400'}`} 
              />
              <h2 className={`text-xl font-semibold mb-2 ${isDark ? 'text-white' : 'text-gray-900'}`}>
                Upload Your Resume
              </h2>
              <p className={isDark ? 'text-gray-400' : 'text-gray-600'}>
                Upload a PDF file to start editing and adding comments
              </p>
              <label className={`
                mt-6 px-6 py-3 rounded-lg inline-flex items-center gap-2 cursor-pointer
                ${isDark
                  ? 'bg-blue-500 text-white hover:bg-blue-600'
                  : 'bg-blue-600 text-white hover:bg-blue-700'
                }
              `}>
                <Upload size={16} />
                Choose PDF
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileChange}
                  className="hidden"
                />
              </label>
            </div>
          )}
        </div>

        {/* Annotations Panel */}
        {file && (
          <div className={`
            w-80 border-l overflow-y-auto flex-shrink-0
            ${isDark ? 'bg-gray-900 border-gray-700' : 'bg-white border-gray-200'}
          `}>
            <div className="p-4">
              <h2 className={`text-lg font-semibold mb-4 ${isDark ? 'text-white' : 'text-gray-900'}`}>
                Comments
              </h2>
              
              {annotations.length === 0 ? (
                <div className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
                  No comments yet. Click the "Add Comment" button to get started.
                </div>
              ) : (
                <div className="space-y-4">
                  {annotations.map(annotation => (
                    <div
                      key={annotation.id}
                      className={`
                        p-4 rounded-lg
                        ${isDark ? 'bg-gray-800' : 'bg-gray-50'}
                      `}
                    >
                      <div className="flex items-start justify-between gap-2">
                        <div className={`text-xs font-medium ${isDark ? 'text-gray-400' : 'text-gray-500'}`}>
                          Page {annotation.pageNumber}
                        </div>
                        <button
                          onClick={() => handleAnnotationDelete(annotation.id)}
                          className={`
                            p-1 rounded hover:bg-red-100 hover:text-red-600 transition-colors
                            ${isDark ? 'text-gray-400' : 'text-gray-500'}
                          `}
                        >
                          <Trash2 size={14} />
                        </button>
                      </div>
                      <p className={`mt-2 text-sm ${isDark ? 'text-gray-300' : 'text-gray-700'}`}>
                        {annotation.text}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}