{{/*
Expand the name of the chart.
*/}}
{{- define "inventory-app.name" -}}
{{- .Values.fullname | default .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }} #If fullname is empty, fallback to Chart.Name (from Chart.yaml → inventory-app)

{{/*
Create a default fully qualified app name.
*/}}
{{- define "inventory-app.fullname" -}}
{{- .Values.fullname | default .Release.Name | trunc 63 | trimSuffix "-" }}
{{- end }} #If empty, use the Helm release name (e.g., app-release or db-release)

{{/*
Create chart name and version as used by the chart label. inventory-app-1.0.0
*/}}
{{- define "inventory-app.chart" -}}  
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }} 

{{/*
Common labels
*/}}
{{- define "inventory-app.labels" -}}
helm.sh/chart: {{ include "inventory-app.chart" . }}
{{ include "inventory-app.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "inventory-app.selectorLabels" -}}
app.kubernetes.io/name: {{ include "inventory-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app: {{ .Values.labels.app }}
tier: {{ .Values.labels.tier }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "inventory-app.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "inventory-app.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
