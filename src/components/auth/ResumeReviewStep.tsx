import React, { useState, useRef, useEffect, KeyboardEvent } from "react";
import {
  User,
  Mail,
  Phone,
  MapPin,
  Linkedin,
  School2,
  Building,
  Calendar,
  X,
  Check,
  Pencil,
} from "lucide-react";
import { ResumeData } from "../../types/auth/types";

interface ResumeReviewStepProps {
  resumeData: ResumeData;
  /**
   * Optional callback if parent needs the mutated/edited data
   */
  onChange?: (data: ResumeData) => void;
}

/**
 * A tiny inline-editable text/textarea.
 * Switches to an <input> (single-line) or <textarea> (multi-line) on click.
 */
function EditableText({
  value,
  onChange,
  className = "",
  multiline = false,
}: {
  value: string;
  onChange: (val: string) => void;
  className?: string;
  multiline?: boolean;
}) {
  const [editing, setEditing] = useState(false);
  const [local, setLocal] = useState(value);
  const ref = useRef<HTMLInputElement | HTMLTextAreaElement>(null);

  // Auto-focus when entering edit mode
  useEffect(() => {
    if (editing && ref.current) ref.current.focus();
  }, [editing]);

  const finish = () => {
    setEditing(false);
    if (local !== value) onChange(local.trim());
  };

  const handleKey = (e: KeyboardEvent) => {
    if (!multiline && e.key === "Enter") {
      e.preventDefault();
      finish();
    } else if (e.key === "Escape") {
      setLocal(value); // revert
      setEditing(false);
    }
  };

  if (editing) {
    return multiline ? (
      <textarea
        ref={ref as React.RefObject<HTMLTextAreaElement>}
        className={`w-full resize-none rounded-md border border-gray-300 bg-white p-1 text-sm shadow-sm focus:border-blue-500 focus:outline-none ${className}`}
        rows={3}
        value={local}
        onChange={(e) => setLocal(e.target.value)}
        onBlur={finish}
        onKeyDown={handleKey}
      />
    ) : (
      <input
        ref={ref as React.RefObject<HTMLInputElement>}
        className={`rounded-md border border-gray-300 bg-white p-1 text-sm shadow-sm focus:border-blue-500 focus:outline-none ${className}`}
        value={local}
        onChange={(e) => setLocal(e.target.value)}
        onBlur={finish}
        onKeyDown={handleKey}
      />
    );
  }

  return (
    <span
      className={`inline-block cursor-text rounded hover:bg-blue-50 ${className}`}
      onClick={() => setEditing(true)}
    >
      {value || <span className="text-gray-400 italic">(empty)</span>}
    </span>
  );
}

export function ResumeReviewStep({ resumeData, onChange }: ResumeReviewStepProps) {
  // Local editable copy
  const [data, setData] = useState(resumeData);

  const update = (path: (string | number)[], val: string) => {
    // Deep clone utility
    const newData: ResumeData = JSON.parse(JSON.stringify(data));
    let cur: any = newData;
    for (let i = 0; i < path.length - 1; i++) cur = cur[path[i]];
    cur[path[path.length - 1]] = val;
    setData(newData);
    onChange?.(newData);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <h3 className="mb-2 text-lg font-semibold text-gray-900">Does this look right?</h3>
        <p className="text-sm text-gray-600">We've extracted this information from your resume – click any field to edit.</p>
      </div>

      {/* Main Card */}
      <div className="relative">
        {/* Edit icon in top right */}
        <button
          type="button"
          className="absolute top-2 right-2 z-10 p-1 rounded hover:bg-gray-200 transition-colors"
          title="Edit"
        >
          <Pencil size={16} className="text-gray-500" />
        </button>
        <div className="max-h-80 space-y-4 overflow-y-auto rounded-lg bg-gray-50 p-4">
          {/* Contact Information */}
          <div>
            <h4 className="mb-2 flex items-center font-medium text-gray-900">
              <User size={16} className="mr-2" />
              <EditableText
                value={data.name}
                onChange={(v) => update(["name"], v)}
                className="font-medium"
              />
            </h4>
            <div className="ml-6 space-y-1 text-sm text-gray-600">
              <div className="flex items-center">
                <Mail size={14} className="mr-2" />
                <EditableText value={data.contact.email} onChange={(v) => update(["contact", "email"], v)} />
              </div>
              <div className="flex items-center">
                <Phone size={14} className="mr-2" />
                <EditableText value={data.contact.phone} onChange={(v) => update(["contact", "phone"], v)} />
              </div>
              <div className="flex items-center">
                <MapPin size={14} className="mr-2" />
                <EditableText value={data.contact.location} onChange={(v) => update(["contact", "location"], v)} />
              </div>
              <div className="flex items-center">
                <Linkedin size={14} className="mr-2" />
                <EditableText value={data.contact.linkedin} onChange={(v) => update(["contact", "linkedin"], v)} />
              </div>
            </div>
          </div>

          {/* Education */}
          <div>
            <h4 className="mb-2 flex items-center font-medium text-gray-900">
              <School2 size={16} className="mr-2" /> Education
            </h4>
            {data.education.map((edu, idx) => (
              <div key={idx} className="mb-3 ml-6 space-y-0.5 text-sm">
                <EditableText
                  value={edu.institution}
                  onChange={(v) => update(["education", idx, "institution"], v)}
                  className="font-medium"
                />
                <EditableText
                  value={edu.degree}
                  onChange={(v) => update(["education", idx, "degree"], v)}
                />
                <div className="flex items-center text-xs text-gray-500">
                  <Calendar size={12} className="mr-1" />
                  <EditableText
                    value={edu.dates}
                    onChange={(v) => update(["education", idx, "dates"], v)}
                  />
                  <span className="mx-1">•</span>
                  GPA:&nbsp;
                  <EditableText
                    value={edu.gpa}
                    onChange={(v) => update(["education", idx, "gpa"], v)}
                  />
                </div>
              </div>
            ))}
          </div>

          {/* Experience */}
          <div>
            <h4 className="mb-2 flex items-center font-medium text-gray-900">
              <Building size={16} className="mr-2" /> Experience
            </h4>
            {data.experience.map((exp, idx) => (
              <div key={idx} className="mb-4 ml-6 text-sm">
                <EditableText
                  value={exp.title}
                  onChange={(v) => update(["experience", idx, "title"], v)}
                  className="font-medium"
                />
                <div className="text-blue-600">
                  <EditableText
                    value={exp.company}
                    onChange={(v) => update(["experience", idx, "company"], v)}
                  />
                </div>
                <div className="mb-2 flex items-center text-xs text-gray-500">
                  <Calendar size={12} className="mr-1" />
                  <EditableText
                    value={exp.dates}
                    onChange={(v) => update(["experience", idx, "dates"], v)}
                  />
                </div>
                {/* Multiline description */}
                <EditableText
                  value={exp.description}
                  onChange={(v) => update(["experience", idx, "description"], v)}
                  multiline
                  className="text-gray-600 leading-relaxed text-xs"
                />
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}