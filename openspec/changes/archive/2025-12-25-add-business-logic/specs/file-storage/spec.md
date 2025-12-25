## ADDED Requirements

### Requirement: Storage Backend Abstraction

The system SHALL provide a storage service with pluggable backends.

#### Scenario: Configure local storage backend

- **WHEN** `STORAGE_BACKEND=local` is set
- **THEN** files SHALL be saved to `/data/images/` directory
- **AND** file URLs SHALL be served via `/api/files/{path}`

#### Scenario: Configure S3 storage backend

- **WHEN** `STORAGE_BACKEND=s3` is set with AWS credentials
- **THEN** files SHALL be uploaded to the configured S3 bucket
- **AND** file URLs SHALL be S3 presigned URLs or public URLs

### Requirement: File Upload

The system SHALL accept file uploads and store them in the configured backend.

#### Scenario: Upload image file successfully

- **WHEN** an image file is uploaded via the storage service
- **THEN** the file SHALL be saved with a unique path
- **AND** the accessible URL SHALL be returned

#### Scenario: File path generation

- **WHEN** a file is uploaded for a product
- **THEN** the path SHALL follow format `products/{product_id}/{filename}`

### Requirement: File Serving (Local Backend)

The system SHALL serve uploaded files when using local storage.

#### Scenario: Serve uploaded file

- **WHEN** a GET request is made to `/api/files/{path}`
- **THEN** the file content SHALL be returned with appropriate content-type

#### Scenario: File not found

- **WHEN** a GET request is made to `/api/files/{invalid_path}`
- **THEN** the response status code SHALL be 404

### Requirement: File Deletion

The system SHALL allow deleting uploaded files.

#### Scenario: Delete file successfully

- **WHEN** a file is deleted via the storage service
- **THEN** the file SHALL be removed from storage
- **AND** subsequent requests for that file SHALL return 404

### Requirement: Supported File Types

The system SHALL validate uploaded file types.

#### Scenario: Accept valid image types

- **WHEN** a file with MIME type image/jpeg, image/png, or image/webp is uploaded
- **THEN** the upload SHALL succeed

#### Scenario: Reject invalid file types

- **WHEN** a file with unsupported MIME type is uploaded
- **THEN** the upload SHALL be rejected with status 400

